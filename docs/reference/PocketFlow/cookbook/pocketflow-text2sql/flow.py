from pocketflow import Flow, Node
from nodes import GetSchema, GenerateSQL, ExecuteSQL, DebugSQL

def create_text_to_sql_flow():
    """Creates the text-to-SQL workflow with a debug loop."""
    get_schema_node = GetSchema()
    generate_sql_node = GenerateSQL()
    execute_sql_node = ExecuteSQL()
    debug_sql_node = DebugSQL()

    # Define the main flow sequence using the default transition operator
    get_schema_node >> generate_sql_node >> execute_sql_node

    # --- Define the debug loop connections using the correct operator ---
    # If ExecuteSQL returns "error_retry", go to DebugSQL
    execute_sql_node - "error_retry" >> debug_sql_node

    # If DebugSQL returns "default", go back to ExecuteSQL
    # debug_sql_node - "default" >> execute_sql_node # Explicitly for "default"
    # OR using the shorthand for default:
    debug_sql_node >> execute_sql_node

    # Create the flow
    text_to_sql_flow = Flow(start=get_schema_node)
    return text_to_sql_flow