"""
Tests for Universal Intelligence integration in Universal Agents.
"""
import unittest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from universal_agents.node import Node
from universal_agents.flow import Flow
from universal_agents.universal_integration import (
    UniversalModelNode,
    UniversalToolNode,
    UniversalAgentNode
)
from universal_intelligence.core.universal_model import AbstractUniversalModel
from universal_intelligence.core.universal_tool import AbstractUniversalTool
from universal_intelligence.core.universal_agent import AbstractUniversalAgent


# Mock Universal Intelligence components for testing
class MockUniversalModel(AbstractUniversalModel):
    """Mock Universal Model for testing."""
    
    def __init__(self, output="mock_model_output"):
        self.output = output
        self.last_prompt = None
        self.last_config = None
    
    def generate(self, prompt, **kwargs):
        self.last_prompt = prompt
        self.last_config = kwargs
        return self.output
    
    @classmethod
    def load(cls, **kwargs):
        return cls()
    
    def unload(self):
        pass
    
    @classmethod
    def requirements(cls):
        return {}
    
    @classmethod
    def compatibility(cls):
        return ["cpu", "gpu"]
    
    @classmethod
    def contract(cls):
        return {
            "class": "text-generation",
            "version": "1.0.0",
            "description": "Mock model for testing."
        }


class MockUniversalTool(AbstractUniversalTool):
    """Mock Universal Tool for testing."""
    
    def __init__(self, return_value="mock_tool_result"):
        self.return_value = return_value
        self.last_args = None
        self.last_kwargs = None
    
    def execute(self, method_name, *args, **kwargs):
        self.last_args = args
        self.last_kwargs = kwargs
        return self.return_value
    
    @classmethod
    def load(cls, **kwargs):
        return cls()
    
    def unload(self):
        pass
    
    def reset(self):
        pass
    
    @classmethod
    def requirements(cls):
        return {}
    
    @classmethod
    def compatibility(cls):
        return ["cpu", "gpu"]
    
    @classmethod
    def contract(cls):
        return {
            "class": "tool",
            "version": "1.0.0",
            "description": "Mock tool for testing.",
            "methods": {
                "test_method": {
                    "description": "Test method",
                    "parameters": {
                        "param1": {"type": "string"},
                        "param2": {"type": "number"}
                    },
                    "returns": {"type": "string"}
                }
            }
        }


class MockUniversalAgent(AbstractUniversalAgent):
    """Mock Universal Agent for testing."""
    
    def __init__(self, output="mock_agent_output"):
        self.output = output
        self._loaded = False
        self.last_input = None
        self.last_config = None
    
    def process(self, input, configuration=None):
        self.last_input = input
        self.last_config = configuration
        return self.output, {"log": "Agent processed input"}
    
    def load(self, **kwargs):
        self._loaded = True
        return self
    
    def loaded(self):
        return self._loaded
    
    def unload(self):
        self._loaded = False
    
    def reset(self):
        pass
    
    def connect(self, component_type, component):
        pass
    
    def disconnect(self, component_type):
        pass
    
    @classmethod
    def requirements(cls):
        return {}
    
    @classmethod
    def compatibility(cls):
        return ["cpu", "gpu"]
    
    @classmethod
    def contract(cls):
        return {
            "class": "agent",
            "version": "1.0.0",
            "description": "Mock agent for testing."
        }


class TestUniversalIntegration(unittest.TestCase):
    
    def test_universal_model_node(self):
        """Test the UniversalModelNode for integrating Universal Models."""
        # Create a mock model
        mock_model = MockUniversalModel(output="This is a test response")
        
        # Create a model node
        model_node = UniversalModelNode(
            model=mock_model,
            prompt_template="Hello, {name}!",
            input_keys=["name"],
            output_key="model_output",
            name="test_model_node"
        )
        
        # Run the node
        shared = {"name": "World"}
        action = model_node.run(shared)
        
        # Verify the node's behavior
        self.assertEqual(mock_model.last_prompt, "Hello, World!")
        self.assertEqual(shared["model_output"], "This is a test response")
        self.assertEqual(action, "next")
    
    def test_universal_tool_node(self):
        """Test the UniversalToolNode for integrating Universal Tools."""
        # Create a mock tool
        mock_tool = MockUniversalTool(return_value="Tool result")
        
        # Create a tool node
        tool_node = UniversalToolNode(
            tool=mock_tool,
            method_name="test_method",
            input_mapping={"param1": "input_param1", "param2": "input_param2"},
            output_key="tool_output",
            name="test_tool_node"
        )
        
        # Run the node
        shared = {"input_param1": "value1", "input_param2": 42}
        action = tool_node.run(shared)
        
        # Verify the node's behavior
        self.assertEqual(mock_tool.last_kwargs, {"param1": "value1", "param2": 42})
        self.assertEqual(shared["tool_output"], "Tool result")
        self.assertEqual(action, "next")
    
    def test_universal_agent_node(self):
        """Test the UniversalAgentNode for integrating Universal Agents."""
        # Create a mock agent
        mock_agent = MockUniversalAgent(output="Agent response")
        
        # Create an agent node
        agent_node = UniversalAgentNode(
            agent=mock_agent,
            input_key="agent_input",
            output_key="agent_output",
            name="test_agent_node"
        )
        
        # Run the node
        shared = {"agent_input": "Process this"}
        action = agent_node.run(shared)
        
        # Verify the node's behavior
        self.assertEqual(mock_agent.last_input, "Process this")
        self.assertEqual(shared["agent_output"], "Agent response")
        self.assertEqual(action, "next")
    
    def test_integrated_flow(self):
        """Test a flow that integrates all Universal components."""
        # Create mock components
        mock_model = MockUniversalModel(output="Model output")
        mock_tool = MockUniversalTool(return_value="Tool result")
        mock_agent = MockUniversalAgent(output="Agent output")
        
        # Create nodes
        model_node = UniversalModelNode(
            model=mock_model,
            prompt_template="Input: {user_query}",
            input_keys=["user_query"],
            output_key="model_output",
            name="model_node"
        )
        
        tool_node = UniversalToolNode(
            tool=mock_tool,
            method_name="test_method",
            input_mapping={"param1": "model_output", "param2": "count"},
            output_key="tool_output",
            name="tool_node"
        )
        
        agent_node = UniversalAgentNode(
            agent=mock_agent,
            input_key="tool_output",
            output_key="final_output",
            name="agent_node"
        )
        
        # Connect nodes
        model_node - "next" >> tool_node
        tool_node - "next" >> agent_node
        
        # Create flow
        flow = Flow(start=model_node, name="integrated_flow")
        
        # Run the flow
        shared = {
            "user_query": "Test query",
            "count": 5
        }
        flow.run(shared)
        
        # Verify the flow's behavior
        self.assertEqual(mock_model.last_prompt, "Input: Test query")
        self.assertEqual(mock_tool.last_kwargs, {"param1": "Model output", "param2": 5})
        self.assertEqual(mock_agent.last_input, "Tool result")
        self.assertEqual(shared["final_output"], "Agent output")
    
    def test_model_node_with_config(self):
        """Test UniversalModelNode with model configuration."""
        # Create a mock model
        mock_model = MockUniversalModel(output="Response with config")
        
        # Create a model node with specific configuration
        model_node = UniversalModelNode(
            model=mock_model,
            prompt_template="Query: {query}",
            input_keys=["query"],
            output_key="response",
            model_parameters={"temperature": 0.7, "max_tokens": 100},
            name="config_model_node"
        )
        
        # Run the node
        shared = {"query": "Test query"}
        model_node.run(shared)
        
        # Verify the model configuration was passed correctly
        self.assertEqual(mock_model.last_config, {"temperature": 0.7, "max_tokens": 100})
        self.assertEqual(shared["response"], "Response with config")


if __name__ == '__main__':
    unittest.main()