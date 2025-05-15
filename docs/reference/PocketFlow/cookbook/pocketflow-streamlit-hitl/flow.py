from pocketflow import Flow
from nodes import InitialInputNode, ProcessDataNode, PrepareFinalResultNode

def create_initial_processing_flow():
    """Creates a flow for the initial data processing stage."""
    initial_input_node = InitialInputNode()
    process_data_node = ProcessDataNode()

    # Define transitions: Input -> Process
    initial_input_node >> process_data_node

    # Create the Flow, starting with the input node
    flow = Flow(start=initial_input_node)
    print("Initial processing flow created.")
    return flow

def create_finalization_flow():
    """Creates a flow to finalize the result after approval."""
    prepare_final_result_node = PrepareFinalResultNode()

    # This flow only has one node
    flow = Flow(start=prepare_final_result_node)
    print("Finalization flow created.")
    return flow
