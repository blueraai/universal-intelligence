"""Mocks for Universal Intelligence components.

This module provides mock implementations of Universal Intelligence
components for testing Universal Agents.
"""

from typing import Any, Callable, Dict, List, Optional, Tuple, Union


class MockUniversalModel:
    """Mock implementation of a Universal Intelligence model."""
    
    def __init__(self, output: str = "Mock model output"):
        """Initialize a new mock model.
        
        Args:
            output: The output that the model will always return
        """
        self.output = output
        self.last_prompt = None
        self.last_config = {}
    
    def contract(self) -> Dict[str, Any]:
        """Return the model contract."""
        return {
            "name": "MockModel",
            "description": "A mock model for testing",
            "capabilities": ["text_generation"]
        }
    
    def process(self, prompt: str, **kwargs) -> Tuple[str, Dict[str, Any]]:
        """Process a prompt and return the output.
        
        Args:
            prompt: The prompt to process
            **kwargs: Additional arguments
            
        Returns:
            A tuple of (output, logs)
        """
        self.last_prompt = prompt
        self.last_config = {k: v for k, v in kwargs.items() if k not in ["stream", "streaming_callback"]}
        
        if "stream" in kwargs and kwargs["stream"] and "streaming_callback" in kwargs:
            callback = kwargs["streaming_callback"]
            # Simulate streaming by calling the callback with chunks
            words = self.output.split()
            for word in words:
                callback(word + " ")
        
        return self.output, {"tokens": len(prompt.split())}


class MockUniversalTool:
    """Mock implementation of a Universal Intelligence tool."""
    
    def __init__(self, return_value: Any = None):
        """Initialize a new mock tool.
        
        Args:
            return_value: The value that the tool will always return
        """
        self.return_value = return_value
        self.last_method = None
        self.last_args = []
        self.last_kwargs = {}
    
    def contract(self) -> Dict[str, Any]:
        """Return the tool contract."""
        return {
            "name": "MockTool",
            "description": "A mock tool for testing",
            "methods": [
                {
                    "name": "test_method",
                    "description": "A test method",
                    "asynchronous": False,
                    "arguments": [
                        {
                            "name": "param1",
                            "type": "string",
                            "description": "First parameter",
                            "required": True
                        },
                        {
                            "name": "param2",
                            "type": "number",
                            "description": "Second parameter",
                            "required": False
                        }
                    ]
                },
                {
                    "name": "retrieve",
                    "description": "Retrieve documents",
                    "asynchronous": False,
                    "arguments": [
                        {
                            "name": "query",
                            "type": "string",
                            "description": "Search query",
                            "required": True
                        },
                        {
                            "name": "top_k",
                            "type": "number",
                            "description": "Number of results",
                            "required": False
                        }
                    ]
                }
            ]
        }
    
    def test_method(self, *args, **kwargs) -> Tuple[Any, Dict[str, Any]]:
        """A test method for mock operations."""
        self.last_method = "test_method"
        self.last_args = args
        self.last_kwargs = kwargs
        return self.return_value, {"method": "test_method"}
    
    def retrieve(self, query: str, top_k: int = 3) -> Tuple[Any, Dict[str, Any]]:
        """Retrieve documents based on a query."""
        self.last_method = "retrieve"
        self.last_args = []
        self.last_kwargs = {"query": query, "top_k": top_k}
        return self.return_value, {"method": "retrieve", "query": query, "top_k": top_k}


class MockUniversalAgent:
    """Mock implementation of a Universal Intelligence agent."""
    
    def __init__(self, output: str = "Mock agent output"):
        """Initialize a new mock agent.
        
        Args:
            output: The output that the agent will always return
        """
        self.output = output
        self.last_input = None
        self.last_config = {}
    
    def contract(self) -> Dict[str, Any]:
        """Return the agent contract."""
        return {
            "name": "MockAgent",
            "description": "A mock agent for testing",
            "capabilities": ["text_processing"]
        }
    
    def process(self, input: str, **kwargs) -> Tuple[str, Dict[str, Any]]:
        """Process input and return the output.
        
        Args:
            input: The input to process
            **kwargs: Additional arguments
            
        Returns:
            A tuple of (output, logs)
        """
        self.last_input = input
        self.last_config = {k: v for k, v in kwargs.items() if k not in ["stream", "streaming_callback"]}
        
        if "stream" in kwargs and kwargs["stream"] and "streaming_callback" in kwargs:
            callback = kwargs["streaming_callback"]
            # Simulate streaming by calling the callback with chunks
            words = self.output.split()
            for word in words:
                callback(word + " ")
        
        return self.output, {"input_length": len(input.split())}