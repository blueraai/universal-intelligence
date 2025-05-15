# cookbook/pocketflow-thinking/nodes.py
from pocketflow import Node
import yaml
from utils import call_llm
import textwrap

# Helper function to format structured plan for printing
def format_plan(plan_items, indent_level=0):
    indent = "  " * indent_level
    output = []
    if isinstance(plan_items, list):
        for item in plan_items:
            if isinstance(item, dict):
                status = item.get('status', 'Unknown')
                desc = item.get('description', 'No description')
                result = item.get('result', '')
                mark = item.get('mark', '') # For verification etc.

                # Format the main step line
                line = f"{indent}- [{status}] {desc}"
                if result:
                    line += f": {result}"
                if mark:
                    line += f" ({mark})"
                output.append(line)

                # Recursively format sub-steps if they exist
                sub_steps = item.get('sub_steps')
                if sub_steps:
                    output.append(format_plan(sub_steps, indent_level + 1))
            elif isinstance(item, str): # Basic fallback for string items
                 output.append(f"{indent}- {item}")
            else: # Fallback for unexpected types
                 output.append(f"{indent}- {str(item)}")

    elif isinstance(plan_items, str): # Handle case where plan is just an error string
        output.append(f"{indent}{plan_items}")
    else:
        output.append(f"{indent}# Invalid plan format: {type(plan_items)}")

    return "\n".join(output)

# Helper function to format structured plan for the prompt (simplified view)
def format_plan_for_prompt(plan_items, indent_level=0):
    indent = "  " * indent_level
    output = []
    # Simplified formatting for prompt clarity
    if isinstance(plan_items, list):
        for item in plan_items:
            if isinstance(item, dict):
                status = item.get('status', 'Unknown')
                desc = item.get('description', 'No description')
                line = f"{indent}- [{status}] {desc}"
                output.append(line)
                sub_steps = item.get('sub_steps')
                if sub_steps:
                    # Indicate nesting without full recursive display in prompt
                    output.append(format_plan_for_prompt(sub_steps, indent_level + 1))
            else: # Fallback
                 output.append(f"{indent}- {str(item)}")
    else:
        output.append(f"{indent}{str(plan_items)}")
    return "\n".join(output)


class ChainOfThoughtNode(Node):
    def prep(self, shared):
        problem = shared.get("problem", "")
        thoughts = shared.get("thoughts", [])
        current_thought_number = shared.get("current_thought_number", 0)

        shared["current_thought_number"] = current_thought_number + 1

        # Format previous thoughts and extract last plan structure
        thoughts_text = ""
        last_plan_structure = None # Will store the list of dicts
        if thoughts:
            thoughts_text_list = []
            for i, t in enumerate(thoughts):
                 thought_block = f"Thought {t.get('thought_number', i+1)}:\n"
                 thinking = textwrap.dedent(t.get('current_thinking', 'N/A')).strip()
                 thought_block += f"  Thinking:\n{textwrap.indent(thinking, '    ')}\n"

                 plan_list = t.get('planning', [])
                 # Use the recursive helper for display formatting
                 plan_str_formatted = format_plan(plan_list, indent_level=2)
                 thought_block += f"  Plan Status After Thought {t.get('thought_number', i+1)}:\n{plan_str_formatted}"

                 if i == len(thoughts) - 1:
                     last_plan_structure = plan_list # Keep the actual structure

                 thoughts_text_list.append(thought_block)

            thoughts_text = "\n--------------------\n".join(thoughts_text_list)
        else:
            thoughts_text = "No previous thoughts yet."
            # Suggest an initial plan structure using dictionaries
            last_plan_structure = [
                {'description': "Understand the problem", 'status': "Pending"},
                {'description': "Develop a high-level plan", 'status': "Pending"},
                {'description': "Conclusion", 'status': "Pending"}
            ]

        # Format the last plan structure for the prompt context using the specific helper
        last_plan_text_for_prompt = format_plan_for_prompt(last_plan_structure) if last_plan_structure else "# No previous plan available."

        return {
            "problem": problem,
            "thoughts_text": thoughts_text,
            "last_plan_text": last_plan_text_for_prompt,
            "last_plan_structure": last_plan_structure, # Pass the raw structure too if needed for complex updates
            "current_thought_number": current_thought_number + 1,
            "is_first_thought": not thoughts
        }

    def exec(self, prep_res):
        problem = prep_res["problem"]
        thoughts_text = prep_res["thoughts_text"]
        last_plan_text = prep_res["last_plan_text"]
        # last_plan_structure = prep_res["last_plan_structure"] # Can use if needed
        current_thought_number = prep_res["current_thought_number"]
        is_first_thought = prep_res["is_first_thought"]

        # --- Construct Prompt ---
        # Instructions updated for dictionary structure
        instruction_base = textwrap.dedent(f"""
            Your task is to generate the next thought (Thought {current_thought_number}).

            Instructions:
            1.  **Evaluate Previous Thought:** If not the first thought, start `current_thinking` by evaluating Thought {current_thought_number - 1}. State: "Evaluation of Thought {current_thought_number - 1}: [Correct/Minor Issues/Major Error - explain]". Address errors first.
            2.  **Execute Step:** Execute the first step in the plan with `status: Pending`.
            3.  **Maintain Plan (Structure):** Generate an updated `planning` list. Each item should be a dictionary with keys: `description` (string), `status` (string: "Pending", "Done", "Verification Needed"), and optionally `result` (string, concise summary when Done) or `mark` (string, reason for Verification Needed). Sub-steps are represented by a `sub_steps` key containing a *list* of these dictionaries.
            4.  **Update Current Step Status:** In the updated plan, change the `status` of the executed step to "Done" and add a `result` key with a concise summary. If verification is needed based on evaluation, change status to "Verification Needed" and add a `mark`.
            5.  **Refine Plan (Sub-steps):** If a "Pending" step is complex, add a `sub_steps` key to its dictionary containing a list of new step dictionaries (status: "Pending") breaking it down. Keep the parent step's status "Pending" until all sub-steps are "Done".
            6.  **Refine Plan (Errors):** Modify the plan logically based on evaluation findings (e.g., change status, add correction steps).
            7.  **Final Step:** Ensure the plan progresses towards a final step dictionary like `{{'description': "Conclusion", 'status': "Pending"}}`.
            8.  **Termination:** Set `next_thought_needed` to `false` ONLY when executing the step with `description: "Conclusion"`.
        """)

        # Context remains largely the same
        if is_first_thought:
            instruction_context = textwrap.dedent("""
                **This is the first thought:** Create an initial plan as a list of dictionaries (keys: description, status). Include sub-steps via the `sub_steps` key if needed. Then, execute the first step in `current_thinking` and provide the updated plan (marking step 1 `status: Done` with a `result`).
            """)
        else:
            instruction_context = textwrap.dedent(f"""
                **Previous Plan (Simplified View):**
                {last_plan_text}

                Start `current_thinking` by evaluating Thought {current_thought_number - 1}. Then, proceed with the first step where `status: Pending`. Update the plan structure (list of dictionaries) reflecting evaluation, execution, and refinements.
            """)

        # Output format example updated for dictionary structure
        instruction_format = textwrap.dedent("""
            Format your response ONLY as a YAML structure enclosed in ```yaml ... ```:
            ```yaml
            current_thinking: |
              # Evaluation of Thought N: [Assessment] ... (if applicable)
              # Thinking for the current step...
            planning:
              # List of dictionaries (keys: description, status, Optional[result, mark, sub_steps])
              - description: "Step 1"
                status: "Done"
                result: "Concise result summary"
              - description: "Step 2 Complex Task" # Now broken down
                status: "Pending" # Parent remains Pending
                sub_steps:
                  - description: "Sub-task 2a"
                    status: "Pending"
                  - description: "Sub-task 2b"
                    status: "Verification Needed"
                    mark: "Result from Thought X seems off"
              - description: "Step 3"
                status: "Pending"
              - description: "Conclusion"
                status: "Pending"
            next_thought_needed: true # Set to false ONLY when executing the Conclusion step.
            ```
        """)

        # Combine prompt parts
        prompt = textwrap.dedent(f"""
            You are a meticulous AI assistant solving a complex problem step-by-step using a structured plan. You critically evaluate previous steps, refine the plan with sub-steps if needed, and handle errors logically. Use the specified YAML dictionary structure for the plan.

            Problem: {problem}

            Previous thoughts:
            {thoughts_text}
            --------------------
            {instruction_base}
            {instruction_context}
            {instruction_format}
        """)
        # --- End Prompt Construction ---

        response = call_llm(prompt)

        # Simple YAML extraction
        yaml_str = response.split("```yaml")[1].split("```")[0].strip()
        thought_data = yaml.safe_load(yaml_str) # Can raise YAMLError

        # --- Validation (using assert) ---
        assert thought_data is not None, "YAML parsing failed, result is None"
        assert "current_thinking" in thought_data, "LLM response missing 'current_thinking'"
        assert "next_thought_needed" in thought_data, "LLM response missing 'next_thought_needed'"
        assert "planning" in thought_data, "LLM response missing 'planning'"
        assert isinstance(thought_data.get("planning"), list), "LLM response 'planning' is not a list"
        # Optional: Add deeper validation of list items being dicts if needed
        # --- End Validation ---

        # Add thought number
        thought_data["thought_number"] = current_thought_number
        return thought_data


    def post(self, shared, prep_res, exec_res):
        # Add the new thought to the list
        if "thoughts" not in shared:
            shared["thoughts"] = []
        shared["thoughts"].append(exec_res)

        # Extract plan for printing using the updated recursive helper function
        plan_list = exec_res.get("planning", ["Error: Planning data missing."])
        plan_str_formatted = format_plan(plan_list, indent_level=1)

        thought_num = exec_res.get('thought_number', 'N/A')
        current_thinking = exec_res.get('current_thinking', 'Error: Missing thinking content.')
        dedented_thinking = textwrap.dedent(current_thinking).strip()

        # Determine if this is the conclusion step based on description
        is_conclusion = False
        if isinstance(plan_list, list):
             # Check if the currently executed step (likely the last 'Done' or the current 'Pending' if evaluation failed) is Conclusion
             # This logic is approximate - might need refinement based on how LLM handles status updates
             for item in reversed(plan_list): # Check recent items first
                 if isinstance(item, dict) and item.get('description') == "Conclusion":
                     # If Conclusion is Done or it's Pending and we are ending, consider it conclusion
                     if item.get('status') == "Done" or (item.get('status') == "Pending" and not exec_res.get("next_thought_needed", True)):
                         is_conclusion = True
                         break
                 # Simple check, might need nested search if Conclusion could be a sub-step

        # Use is_conclusion flag OR the next_thought_needed flag for termination
        if not exec_res.get("next_thought_needed", True): # Primary termination signal
            shared["solution"] = dedented_thinking # Solution is the thinking content of the final step
            print(f"\nThought {thought_num} (Conclusion):")
            print(f"{textwrap.indent(dedented_thinking, '  ')}")
            print("\nFinal Plan Status:")
            print(textwrap.indent(plan_str_formatted, '  '))
            print("\n=== FINAL SOLUTION ===")
            print(dedented_thinking)
            print("======================\n")
            return "end"

        # Otherwise, continue the chain
        print(f"\nThought {thought_num}:")
        print(f"{textwrap.indent(dedented_thinking, '  ')}")
        print("\nCurrent Plan Status:")
        print(textwrap.indent(plan_str_formatted, '  '))
        print("-" * 50)

        return "continue"