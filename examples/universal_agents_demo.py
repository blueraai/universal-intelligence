"""Universal Agents Demo - Simple Working Example

This script demonstrates a simple functioning example of Universal Agents.
It creates a basic flow with custom nodes and runs it with sample input.
"""

import sys
import os
import logging
from typing import Dict, Any

# Add the repository root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from universal_agents.node import Node, Flow

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class GreetingNode(Node):
    """Node that creates a greeting based on input name."""
    
    def __init__(self, name=None):
        super().__init__(name or "GreetingNode")
    
    def prep(self, shared: Dict[str, Any]) -> str:
        """Extract name from shared state."""
        return shared.get("name", "World")
    
    def exec(self, prep_data: str) -> str:
        """Create greeting message."""
        return f"Hello, {prep_data}!"
    
    def post(self, shared: Dict[str, Any], prep_data: str, exec_result: str) -> str:
        """Store the greeting in shared state."""
        shared["greeting"] = exec_result
        return "next"


class ProcessingNode(Node):
    """Node that transforms the greeting."""
    
    def __init__(self, name=None):
        super().__init__(name or "ProcessingNode")
    
    def prep(self, shared: Dict[str, Any]) -> str:
        """Get greeting from shared state."""
        return shared.get("greeting", "")
    
    def exec(self, prep_data: str) -> str:
        """Transform the greeting."""
        return prep_data.upper()
    
    def post(self, shared: Dict[str, Any], prep_data: str, exec_result: str) -> str:
        """Store transformed greeting."""
        shared["transformed_greeting"] = exec_result
        return "complete"


def main():
    """Main function that runs the demo."""
    print("\n=== Universal Agents Demo ===\n")
    
    try:
        # Create nodes
        greeting_node = GreetingNode()
        processing_node = ProcessingNode()
        
        # Connect nodes
        greeting_node - "next" >> processing_node
        
        # Create flow
        flow = Flow(start=greeting_node, name="SimpleGreetingFlow")
        
        # Initialize shared state
        shared = {"name": "Universal Intelligence"}
        
        # Run the flow
        logger.info("Running the flow...")
        result = flow.run(shared)
        
        # Display results
        print(f"\nOriginal Greeting: {result.get('greeting')}")
        print(f"Transformed Greeting: {result.get('transformed_greeting')}")
        print(f"\nFlow completed in {result.get('_flow_steps')} steps")
        print(f"Execution path: {' -> '.join(result.get('_flow_execution_path'))}")
        
        print("\nDemo completed successfully!")
        
    except Exception as e:
        logger.error(f"Error running demo: {str(e)}")
        raise


if __name__ == "__main__":
    main()