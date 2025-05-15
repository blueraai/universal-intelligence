"""Universal Agents Standalone Demo

This script demonstrates a working example of Universal Agents that doesn't
depend on external models or tools. It uses mock classes to simulate the
behavior of Universal Intelligence components.
"""

import sys
import os
import logging
from typing import Dict, Any, List, Optional, Tuple

# Add the repository root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import core Universal Agents components directly without dependencies
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../universal_agents')))
from universal_agents.node import Node, Flow

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Mock Classes to simulate Universal Intelligence components

class MockUniversalModel:
    """Mock implementation of a Universal Intelligence model."""
    
    def contract(self):
        """Return the model contract."""
        return {
            "name": "MockModel",
            "description": "A mock model for demonstration purposes",
            "capabilities": ["text_generation"]
        }
    
    def process(self, prompt: str, **kwargs) -> Tuple[str, Dict[str, Any]]:
        """Process a prompt and return a response."""
        logger.info(f"Processing prompt: {prompt[:50]}...")
        
        # Simple response generation based on the prompt
        if "weather" in prompt.lower():
            response = "The weather today is sunny with a high of 75°F."
        elif "name" in prompt.lower():
            response = "My name is MockModel, a demonstration model for Universal Agents."
        elif "hello" in prompt.lower() or "hi" in prompt.lower():
            response = "Hello! How can I assist you today?"
        else:
            response = f"I received your prompt: '{prompt}'. This is a mock response for demonstration purposes."
            
        return response, {"tokens": len(prompt.split())}


class MockUniversalTool:
    """Mock implementation of a Universal Intelligence tool."""
    
    def contract(self):
        """Return the tool contract."""
        return {
            "name": "MockSearchTool",
            "description": "A mock search tool for demonstration purposes",
            "methods": [
                {
                    "name": "search",
                    "description": "Search for information",
                    "asynchronous": False,
                    "arguments": [
                        {
                            "name": "query",
                            "type": "str",
                            "description": "The search query",
                            "required": True
                        },
                        {
                            "name": "num_results",
                            "type": "int",
                            "description": "Number of results to return",
                            "required": False
                        }
                    ]
                }
            ]
        }
    
    def search(self, query: str, num_results: int = 3) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """Search for information based on a query."""
        logger.info(f"Searching for: {query}")
        
        # Mock search results
        results = [
            {
                "title": f"Result 1 for {query}",
                "content": f"This is the first mock search result for '{query}'.",
                "url": f"https://example.com/1?q={query}"
            },
            {
                "title": f"Result 2 for {query}",
                "content": f"This is the second mock search result for '{query}'.",
                "url": f"https://example.com/2?q={query}"
            },
            {
                "title": f"Result 3 for {query}",
                "content": f"This is the third mock search result for '{query}'.",
                "url": f"https://example.com/3?q={query}"
            }
        ]
        
        return results[:num_results], {"query": query, "total_results": 100}


# Custom Nodes for the demo

class InputNode(Node):
    """Node for handling user input."""
    
    def __init__(self, name: Optional[str] = None):
        super().__init__(name or "InputNode")
    
    def prep(self, shared: Dict[str, Any]) -> str:
        """Get input from shared state or use default."""
        if "user_input" in shared:
            return shared["user_input"]
        return "Tell me about Universal Agents"
    
    def post(self, shared: Dict[str, Any], prep_data: str, exec_result: str) -> str:
        """Store input and determine next action."""
        shared["query"] = exec_result
        
        if "weather" in exec_result.lower():
            return "weather"
        return "search"


class SearchNode(Node):
    """Node that simulates using a Universal Intelligence tool for search."""
    
    def __init__(self, name: Optional[str] = None):
        super().__init__(name or "SearchNode")
        self.tool = MockUniversalTool()
    
    def prep(self, shared: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare search arguments."""
        return {
            "query": shared.get("query", ""),
            "num_results": shared.get("num_results", 2)
        }
    
    def exec(self, prep_data: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """Execute search using the mock tool."""
        return self.tool.search(**prep_data)
    
    def post(self, shared: Dict[str, Any], prep_data: Dict[str, Any], exec_result: Tuple[List[Dict[str, Any]], Dict[str, Any]]) -> str:
        """Process search results."""
        results, logs = exec_result
        
        # Store results in shared state
        shared["search_results"] = results
        shared["search_logs"] = logs
        
        # Create a formatted context from results
        context = "Search Results:\n\n"
        for i, result in enumerate(results):
            context += f"{i+1}. {result['title']}\n{result['content']}\n\n"
        
        shared["context"] = context
        
        return "generate"


class WeatherNode(Node):
    """Node that handles weather-related queries."""
    
    def __init__(self, name: Optional[str] = None):
        super().__init__(name or "WeatherNode")
    
    def prep(self, shared: Dict[str, Any]) -> str:
        """Get query from shared state."""
        return shared.get("query", "")
    
    def exec(self, prep_data: str) -> Dict[str, Any]:
        """Generate mock weather data."""
        location = prep_data.replace("weather", "").replace("in", "").strip()
        if not location:
            location = "the current location"
            
        return {
            "location": location,
            "condition": "sunny",
            "temperature": 75,
            "humidity": 45,
            "wind": "5 mph"
        }
    
    def post(self, shared: Dict[str, Any], prep_data: str, exec_result: Dict[str, Any]) -> str:
        """Process weather data."""
        shared["weather_data"] = exec_result
        
        # Create formatted weather info
        weather_info = f"Weather for {exec_result['location']}:\n"
        weather_info += f"Condition: {exec_result['condition']}\n"
        weather_info += f"Temperature: {exec_result['temperature']}°F\n"
        weather_info += f"Humidity: {exec_result['humidity']}%\n"
        weather_info += f"Wind: {exec_result['wind']}"
        
        shared["context"] = weather_info
        
        return "generate"


class GenerationNode(Node):
    """Node that simulates using a Universal Intelligence model for generation."""
    
    def __init__(self, name: Optional[str] = None):
        super().__init__(name or "GenerationNode")
        self.model = MockUniversalModel()
    
    def prep(self, shared: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare model input."""
        query = shared.get("query", "")
        context = shared.get("context", "")
        
        prompt = f"""Please provide a helpful response based on the following information:

Context:
{context}

User Query:
{query}

Response:"""
        
        return {"prompt": prompt}
    
    def exec(self, prep_data: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """Generate response using the mock model."""
        return self.model.process(prep_data["prompt"])
    
    def post(self, shared: Dict[str, Any], prep_data: Dict[str, Any], exec_result: Tuple[str, Dict[str, Any]]) -> str:
        """Process model output."""
        response, logs = exec_result
        
        shared["response"] = response
        shared["model_logs"] = logs
        
        return "output"


class OutputNode(Node):
    """Node for displaying the final output."""
    
    def __init__(self, name: Optional[str] = None):
        super().__init__(name or "OutputNode")
    
    def prep(self, shared: Dict[str, Any]) -> Dict[str, Any]:
        """Collect data for output."""
        return {
            "query": shared.get("query", ""),
            "response": shared.get("response", "No response generated.")
        }
    
    def post(self, shared: Dict[str, Any], prep_data: Dict[str, Any], exec_result: Dict[str, Any]) -> str:
        """Display output and proceed to completion."""
        print(f"\nQuery: {prep_data['query']}")
        print(f"\nResponse: {prep_data['response']}")
        
        return "complete"


def main():
    """Main function that runs the demo."""
    print("\n=== Universal Agents Standalone Demo ===\n")
    print("This demo shows a working flow that simulates search and response generation.\n")
    
    try:
        # Create nodes
        input_node = InputNode()
        search_node = SearchNode()
        weather_node = WeatherNode()
        generation_node = GenerationNode()
        output_node = OutputNode()
        
        # Connect nodes
        input_node - "search" >> search_node
        input_node - "weather" >> weather_node
        search_node - "generate" >> generation_node
        weather_node - "generate" >> generation_node
        generation_node - "output" >> output_node
        
        # Create flow
        flow = Flow(start=input_node, name="SearchAndGenerateFlow")
        
        # Try with different inputs
        inputs = [
            "Tell me about Universal Agents",
            "What's the weather in San Francisco",
            "Hello, how are you today?"
        ]
        
        for user_input in inputs:
            print(f"\n--- Running with input: '{user_input}' ---")
            
            # Initialize shared state with input
            shared = {"user_input": user_input}
            
            # Run the flow
            logger.info(f"Running flow with input: {user_input}")
            result = flow.run(shared)
            
            # Display execution information
            print(f"\nFlow completed in {result.get('_flow_steps')} steps")
            print(f"Execution path: {' -> '.join(result.get('_flow_execution_path'))}")
            print("-" * 50)
        
        print("\nDemo completed successfully!")
        
    except Exception as e:
        logger.error(f"Error running demo: {str(e)}")
        raise


if __name__ == "__main__":
    main()