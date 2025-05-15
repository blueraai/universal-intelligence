import sys
import os
from flow import create_text_to_sql_flow
from populate_db import populate_database, DB_FILE

def run_text_to_sql(natural_query, db_path=DB_FILE, max_debug_retries=3):
    if not os.path.exists(db_path) or os.path.getsize(db_path) == 0:
        print(f"Database at {db_path} missing or empty. Populating...")
        populate_database(db_path)

    shared = {
        "db_path": db_path,
        "natural_query": natural_query,
        "max_debug_attempts": max_debug_retries,
        "debug_attempts": 0,
        "final_result": None,
        "final_error": None
    }

    print(f"\n=== Starting Text-to-SQL Workflow ===")
    print(f"Query: '{natural_query}'")
    print(f"Database: {db_path}")
    print(f"Max Debug Retries on SQL Error: {max_debug_retries}")
    print("=" * 45)

    flow = create_text_to_sql_flow()
    flow.run(shared) # Let errors inside the loop be handled by the flow logic

    # Check final state based on shared data
    if shared.get("final_error"):
            print("\n=== Workflow Completed with Error ===")
            print(f"Error: {shared['final_error']}")
    elif shared.get("final_result") is not None:
            print("\n=== Workflow Completed Successfully ===")
            # Result already printed by ExecuteSQL node
    else:
            # Should not happen if flow logic is correct and covers all end states
            print("\n=== Workflow Completed (Unknown State) ===")

    print("=" * 36)
    return shared

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = "total products per category"

    run_text_to_sql(query) 