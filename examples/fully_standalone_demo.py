"""Fully Standalone Universal Agents Demo

This script is a completely standalone demonstration of Universal Agents core functionality
without any external dependencies. It includes simplified versions of the Node and Flow
classes to show the core concepts in action.
"""

import logging
from typing import Dict, Any, List, Optional, Callable, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Simplified Universal Agents implementation
class Node:
    """Simplified Node class demonstrating core functionality."""
    
    def __init__(self, name: Optional[str] = None):
        """Initialize a node."""
        self.name = name or self.__class__.__name__
        self.connections = {}
    
    def __sub__(self, action: str) -> 'NodeConnection':
        """Support for node - "action" >> target_node syntax."""
        return NodeConnection(self, action)
    
    def connect(self, action: str, target_node: 'Node') -> 'Node':
        """Connect this node to a target node with the specified action."""
        self.connections[action] = target_node
        return self
    
    def prep(self, shared: Dict[str, Any]) -> Any:
        """Prepare data for execution from shared state."""
        return None
    
    def exec(self, prep_data: Any) -> Any:
        """Execute the core functionality of the node."""
        return prep_data
    
    def post(self, shared: Dict[str, Any], prep_data: Any, exec_result: Any) -> str:
        """Process execution results and determine the next action."""
        return "next"
    
    def run(self, shared: Dict[str, Any]) -> str:
        """Run the complete node lifecycle."""
        prep_data = self.prep(shared)
        exec_result = self.exec(prep_data)
        return self.post(shared, prep_data, exec_result)


class NodeConnection:
    """Helper class for connecting nodes with actions."""
    
    def __init__(self, source: Node, action: str):
        """Initialize a node connection."""
        self.source = source
        self.action = action
    
    def __rshift__(self, target: Node) -> Node:
        """Connect the source node to the target node with the specified action."""
        self.source.connections[self.action] = target
        return self.source


class Flow:
    """Simplified Flow class demonstrating core functionality."""
    
    def __init__(self, start: Node, name: Optional[str] = None):
        """Initialize a flow."""
        self.start = start
        self.name = name or f"flow_{id(self)}"
        self.nodes = self._collect_nodes(start)
    
    def _collect_nodes(self, start: Node) -> List[Node]:
        """Collect all nodes in the flow starting from the start node."""
        nodes = []
        visited = set()
        
        def visit(node: Node) -> None:
            if node in visited:
                return
            
            visited.add(node)
            nodes.append(node)
            
            for target in node.connections.values():
                visit(target)
        
        visit(start)
        return nodes
    
    def run(self, shared: Optional[Dict[str, Any]] = None, max_steps: int = 100) -> Dict[str, Any]:
        """Run the flow starting from the start node."""
        # Initialize shared state
        state = shared.copy() if shared else {}
        
        # Start with the start node
        current_node = self.start
        
        # Track execution path
        step_count = 0
        execution_path = []
        
        # Execute until we reach a node with no connections or hit max_steps
        while current_node and step_count < max_steps:
            # Increment step count
            step_count += 1
            
            # Record execution path
            execution_path.append(current_node.name)
            
            # Log current node execution
            logger.info(f"Executing node: {current_node.name} (step {step_count})")
            
            try:
                # Execute the node's lifecycle methods
                prep_data = current_node.prep(state)
                exec_result = current_node.exec(prep_data)
                action = current_node.post(state, prep_data, exec_result)
                
                logger.info(f"Node {current_node.name} returned action: {action}")
                
                # Find the next node based on the action
                current_node = current_node.connections.get(action)
                
            except Exception as e:
                logger.error(f"Error in node {current_node.name}: {str(e)}")
                state["error"] = str(e)
                state["error_node"] = current_node.name
                
                # Try to find an error handler
                current_node = current_node.connections.get("error")
                
                # If no error handler, stop execution
                if not current_node:
                    logger.error("No error handler found, stopping flow execution")
                    break
        
        # Add information about execution
        state["_flow_completed"] = current_node is None
        state["_flow_steps"] = step_count
        state["_flow_execution_path"] = execution_path
        state["_flow_max_steps_reached"] = step_count >= max_steps
        
        # Log completion
        logger.info(f"Flow {self.name} completed in {step_count} steps")
        
        return state


# Demo Nodes

class InputNode(Node):
    """Node for handling user input."""
    
    def __init__(self, name: Optional[str] = None):
        super().__init__(name or "InputNode")
    
    def prep(self, shared: Dict[str, Any]) -> str:
        """Get input from shared state."""
        return shared.get("input", "Default input")
    
    def post(self, shared: Dict[str, Any], prep_data: str, exec_result: str) -> str:
        """Store the input and proceed to processing."""
        shared["user_input"] = exec_result
        return "process"


class ProcessingNode(Node):
    """Node for processing input."""
    
    def __init__(self, name: Optional[str] = None):
        super().__init__(name or "ProcessingNode")
    
    def prep(self, shared: Dict[str, Any]) -> str:
        """Get user input from shared state."""
        return shared.get("user_input", "")
    
    def exec(self, prep_data: str) -> str:
        """Transform the input."""
        return prep_data.upper()
    
    def post(self, shared: Dict[str, Any], prep_data: str, exec_result: str) -> str:
        """Store the processed input."""
        shared["processed_input"] = exec_result
        
        # Choose next action based on input content
        if "weather" in prep_data.lower():
            return "weather"
        elif "hello" in prep_data.lower():
            return "greeting"
        else:
            return "generate"


class WeatherNode(Node):
    """Node for handling weather queries."""
    
    def __init__(self, name: Optional[str] = None):
        super().__init__(name or "WeatherNode")
    
    def prep(self, shared: Dict[str, Any]) -> str:
        """Get the processed input."""
        return shared.get("processed_input", "")
    
    def exec(self, prep_data: str) -> Dict[str, Any]:
        """Generate weather information."""
        return {
            "condition": "sunny",
            "temperature": 75,
            "humidity": 45
        }
    
    def post(self, shared: Dict[str, Any], prep_data: str, exec_result: Dict[str, Any]) -> str:
        """Format weather information and store it."""
        weather_info = f"Weather is {exec_result['condition']} with a temperature of {exec_result['temperature']}°F and {exec_result['humidity']}% humidity."
        shared["response"] = weather_info
        return "output"


class GreetingNode(Node):
    """Node for generating greetings."""
    
    def __init__(self, name: Optional[str] = None):
        super().__init__(name or "GreetingNode")
    
    def exec(self, prep_data: str) -> str:
        """Generate a greeting."""
        return "Hello! How can I assist you today?"
    
    def post(self, shared: Dict[str, Any], prep_data: str, exec_result: str) -> str:
        """Store the greeting."""
        shared["response"] = exec_result
        return "output"


class GenerationNode(Node):
    """Node for generating responses."""
    
    def __init__(self, name: Optional[str] = None):
        super().__init__(name or "GenerationNode")
    
    def prep(self, shared: Dict[str, Any]) -> str:
        """Get the processed input."""
        return shared.get("processed_input", "")
    
    def exec(self, prep_data: str) -> str:
        """Generate a response based on the input."""
        return f"You said: {prep_data}. This is a demonstration of response generation based on your input."
    
    def post(self, shared: Dict[str, Any], prep_data: str, exec_result: str) -> str:
        """Store the generated response."""
        shared["response"] = exec_result
        return "output"


class OutputNode(Node):
    """Node for displaying the final output."""
    
    def __init__(self, name: Optional[str] = None):
        super().__init__(name or "OutputNode")
    
    def prep(self, shared: Dict[str, Any]) -> Dict[str, Any]:
        """Collect data for output."""
        return {
            "input": shared.get("user_input", ""),
            "response": shared.get("response", "No response generated.")
        }
    
    def exec(self, prep_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format the output."""
        return prep_data
    
    def post(self, shared: Dict[str, Any], prep_data: Dict[str, Any], exec_result: Dict[str, Any]) -> str:
        """Display the output."""
        print(f"\nUser Input: {exec_result['input']}")
        print(f"Response: {exec_result['response']}")
        return "complete"


def run_demo(input_text: str) -> Dict[str, Any]:
    """Run the demo with the given input."""
    print(f"\n--- Running with input: '{input_text}' ---")
    
    # Create nodes
    input_node = InputNode()
    processing_node = ProcessingNode()
    weather_node = WeatherNode()
    greeting_node = GreetingNode()
    generation_node = GenerationNode()
    output_node = OutputNode()
    
    # Connect nodes
    input_node - "process" >> processing_node
    processing_node - "weather" >> weather_node
    processing_node - "greeting" >> greeting_node
    processing_node - "generate" >> generation_node
    weather_node - "output" >> output_node
    greeting_node - "output" >> output_node
    generation_node - "output" >> output_node
    
    # Create flow
    flow = Flow(start=input_node, name="DemoFlow")
    
    # Initialize shared state
    shared = {"input": input_text}
    
    # Run the flow
    result = flow.run(shared)
    
    # Display execution information
    print(f"Flow completed in {result.get('_flow_steps')} steps")
    print(f"Execution path: {' -> '.join(result.get('_flow_execution_path'))}")
    print("-" * 50)
    
    return result


def main():
    """Main function that runs the demo."""
    print("\n=== Fully Standalone Universal Agents Demo ===\n")
    print("This demo shows a simplified version of Universal Agents core functionality.")
    print("It includes a complete implementation of Node and Flow classes without any dependencies.\n")
    
    # Run with different inputs to demonstrate various paths
    inputs = [
        "Hello, how are you?",
        "What's the weather like today?",
        "Tell me something interesting"
    ]
    
    for input_text in inputs:
        run_demo(input_text)
    
    print("\nDemo completed successfully!")


if __name__ == "__main__":
    main()