from pocketflow import Node
from utils.process_task import process_task

class InitialInputNode(Node):
    """Reads the initial task input from shared_data."""
    def prep(self, shared):
        print("InitialInputNode: Prep")
        return shared.get("task_input", "Default Task Input")

    def exec(self, prep_res):
        print(f"InitialInputNode: Executing with input: '{prep_res[:50]}...'")
        # No real computation needed here, just passing the input along
        return prep_res

    def post(self, shared, prep_res, exec_res):
        # Ensure the input used is stored, although it might already be there
        shared["input_used_by_process"] = exec_res
        print(f"InitialInputNode: Post - Stored input '{exec_res[:50]}...' in shared_data.")
        return "default" # Proceed to next node in the flow

class ProcessDataNode(Node):
    """Processes the data using the utility function."""
    def prep(self, shared):
        task_input = shared.get("input_used_by_process", "No input found")
        print(f"ProcessDataNode: Prep - Input: '{task_input[:50]}...'")
        return task_input

    def exec(self, prep_res):
        print("ProcessDataNode: Exec - Calling process_task utility")
        # Call the actual processing logic
        processed_output = process_task(prep_res)
        return processed_output

    def post(self, shared, prep_res, exec_res):
        # Store the result for review
        shared["processed_output"] = exec_res
        print(f"ProcessDataNode: Post - Stored processed output: '{str(exec_res)[:50]}...'")
        # This node ends the initial processing subflow
        return None

class PrepareFinalResultNode(Node):
    """Takes the approved processed output and sets it as the final result."""
    def prep(self, shared):
        approved_output = shared.get("processed_output", "No processed output found")
        print(f"PrepareFinalResultNode: Prep - Approved output: '{str(approved_output)[:50]}...'")
        return approved_output

    def exec(self, prep_res):
        print("PrepareFinalResultNode: Exec - Finalizing result.")
        # Could potentially do final formatting here if needed
        return prep_res

    def post(self, shared, prep_res, exec_res):
        shared["final_result"] = exec_res
        print(f"PrepareFinalResultNode: Post - Stored final result: '{str(exec_res)[:50]}...'")
        # This node ends the finalization subflow
        return None