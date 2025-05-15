import time

def process_task(input_data):
    """Minimal simulation of processing the input data."""
    print(f"Processing: '{input_data[:50]}...'")
    
    # Simulate work
    time.sleep(2)

    processed_result = f"Processed: {input_data}"
    print(f"Finished processing.")
    return processed_result

# We don't need a separate utils/call_llm.py for this minimal example,
# but you would add it here if ProcessNode used an LLM.

