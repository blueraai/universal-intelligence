"""
Tests for the design pattern implementations in Universal Agents.
"""
import unittest
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from universal_agents.node import Node
from universal_agents.flow import Flow
from universal_agents.patterns import (
    create_rag_flow,
    MapNode, ModelMapNode, ReduceNode, ModelReduceNode, create_map_reduce_flow,
    create_multi_agent_flow,
    create_conditional_workflow
)
from .mocks.mock_universal import (
    MockUniversalModel,
    MockUniversalTool,
    MockUniversalAgent
)


class TestPatternImplementations(unittest.TestCase):
    
    def test_rag_pattern(self):
        """Test the RAG pattern implementation."""
        # Create mock components
        mock_model = MockUniversalModel(output="Generated response")
        mock_tool = MockUniversalTool(return_value=["Document 1", "Document 2"])
        
        # Create RAG flow
        rag_flow = create_rag_flow(
            retrieval_tool=mock_tool,
            retrieval_method="retrieve",
            generation_model=mock_model,
            retrieval_arg_mapping={"query": "user_query"},
            name="test_rag_flow"
        )
        
        # Run the flow
        shared = {"user_query": "Test query"}
        result = rag_flow.run(shared)
        
        # Verify the flow's behavior
        self.assertEqual(mock_tool.last_method, "retrieve")
        self.assertEqual(mock_tool.last_kwargs, {"query": "Test query"})
        self.assertIn("Document 1", mock_model.last_prompt)
        self.assertIn("Document 2", mock_model.last_prompt)
        self.assertEqual(shared["generation_output"], "Generated response")
    
    def test_map_reduce_pattern(self):
        """Test the Map-Reduce pattern implementation."""
        # Create a simple map function
        def square(x):
            return x * x
        
        # Create a simple reduce function
        def sum_values(values):
            return sum(values)
        
        # Create map node
        map_node = MapNode(
            map_fn=square,
            input_key="input_values",
            output_key="squared_values",
            name="square_map_node"
        )
        
        # Create reduce node
        reduce_node = ReduceNode(
            reduce_fn=sum_values,
            input_key="squared_values",
            output_key="sum_of_squares",
            name="sum_reduce_node"
        )
        
        # Connect nodes
        map_node - "next" >> reduce_node
        
        # Create flow
        flow = Flow(start=map_node, name="map_reduce_flow")
        
        # Run the flow
        shared = {"input_values": [1, 2, 3, 4, 5]}
        flow.run(shared)
        
        # Verify results (sum of squares: 1+4+9+16+25 = 55)
        self.assertEqual(shared["squared_values"], [1, 4, 9, 16, 25])
        self.assertEqual(shared["sum_of_squares"], 55)
    
    def test_model_map_reduce_pattern(self):
        """Test the Map-Reduce pattern with models."""
        # Create mock models
        map_model = MockUniversalModel(output="Mapped item")
        reduce_model = MockUniversalModel(output="Reduced result")
        
        # Create map-reduce flow
        flow = create_map_reduce_flow(
            map_model=map_model,
            reduce_model=reduce_model,
            map_prompt_template="Map: {item}",
            reduce_prompt_template="Reduce: {items}",
            name="model_map_reduce_flow"
        )
        
        # Run the flow
        shared = {"items": ["item1", "item2", "item3"]}
        flow.run(shared)
        
        # Verify the flow's behavior
        self.assertIn("items", reduce_model.last_prompt)
        self.assertIn("Mapped item", reduce_model.last_prompt)
        self.assertEqual(shared["result"], "Reduced result")
    
    def test_multi_agent_pattern(self):
        """Test the Multi-Agent pattern implementation."""
        # Create mock components
        coordinator_model = MockUniversalModel(output="research")  # Select research agent
        research_agent = MockUniversalAgent(output="Research findings")
        creative_agent = MockUniversalAgent(output="Creative ideas")
        
        # Create specialist agents dictionary
        specialist_agents = {
            "research": (research_agent, "Research specialist"),
            "creative": (creative_agent, "Creative specialist")
        }
        
        # Create multi-agent flow
        flow = create_multi_agent_flow(
            coordinator_model=coordinator_model,
            specialist_agents=specialist_agents,
            name="multi_agent_flow"
        )
        
        # Run the flow
        shared = {"user_input": "Analyze this topic"}
        result = flow.run(shared)
        
        # Verify the flow's behavior
        self.assertIn("research", coordinator_model.last_prompt.lower())
        self.assertIn("creative", coordinator_model.last_prompt.lower())
        self.assertEqual(research_agent.last_input, "Analyze this topic")
        self.assertEqual(shared["agent_outputs"]["research"], "Research findings")
        self.assertEqual(shared["final_response"], "Research findings")  # Coordinator passes through
    
    def test_conditional_workflow_pattern(self):
        """Test the Conditional Workflow pattern implementation."""
        # Create mock model for decision-making
        decision_model = MockUniversalModel(output="option_a")
        
        # Create simple test nodes
        class ResultNode(Node):
            def __init__(self, result, name=None):
                super().__init__(name=name)
                self.result = result
            
            def exec(self, prep_data):
                return self.result
            
            def post(self, shared, prep_data, exec_result):
                shared["workflow_output"] = exec_result
                return "next"
        
        # Create option nodes
        option_a_nodes = [ResultNode("Option A result", name="option_a_node")]
        option_b_nodes = [ResultNode("Option B result", name="option_b_node")]
        
        # Define options for the workflow
        options = {
            "option_a": (option_a_nodes, "First option"),
            "option_b": (option_b_nodes, "Second option")
        }
        
        # Create conditional workflow
        flow = create_conditional_workflow(
            model=decision_model,
            decision_prompt="Make a decision based on: {input}",
            options=options,
            input_keys=["input"],
            name="conditional_workflow"
        )
        
        # Run the flow
        shared = {"input": "Test input"}
        result = flow.run(shared)
        
        # Verify the flow's behavior
        self.assertIn("input", decision_model.last_prompt)
        self.assertIn("option_a", decision_model.last_prompt.lower())
        self.assertEqual(shared["decision"], "option_a")
        self.assertEqual(shared["result"], "Option A result")


if __name__ == '__main__':
    unittest.main()