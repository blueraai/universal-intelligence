import time

def process_task(task_input: str) -> str:
    """
    Simulates processing the input, potentially calling an LLM.
    Replace this with your actual task logic.
    """
    print(f"Processing task: {task_input[:50]}...")

    result = f"Dummy rephrased text for the following input: {task_input}"

    # Simulate some work
    time.sleep(2) 
    return result

if __name__ == "__main__":
    test_input = "This is a test input for the processing task."
    print(f"Input: {test_input}")
    output = process_task(test_input)
    print(f"Output: {output}")

# We don't need a separate utils/call_llm.py for this minimal example,
# but you would add it here if ProcessNode used an LLM.

