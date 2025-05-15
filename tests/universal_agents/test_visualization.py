"""
Tests for the visualization utilities in Universal Agents.
"""
import unittest
import sys
import os
import tempfile
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from universal_agents.node import Node
from universal_agents.flow import Flow
from universal_agents.visualization import generate_flow_visualization, visualize_execution_path


class NumberNode(Node):
    """A node that stores a number in shared state."""
    def __init__(self, number, name=None):
        super().__init__(name=name)
        self.number = number
    
    def prep(self, shared):
        shared['current'] = self.number
        return self.number
    
    def exec(self, prep_data):
        return prep_data
    
    # post implicitly returns "next" (default action)


class AddNode(Node):
    """A node that adds a number to the current value in shared state."""
    def __init__(self, number, name=None):
        super().__init__(name=name)
        self.number = number
    
    def prep(self, shared):
        if 'current' not in shared:
            shared['current'] = 0
        return shared['current']
    
    def exec(self, prep_data):
        return prep_data + self.number
    
    def post(self, shared, prep_data, exec_result):
        shared['current'] = exec_result
        return "next"


class TestVisualization(unittest.TestCase):
    
    def setUp(self):
        """Set up a sample flow for testing visualization."""
        # Create nodes
        self.start_node = NumberNode(5, name="start")
        self.add_node1 = AddNode(10, name="add_10")
        self.add_node2 = AddNode(20, name="add_20")
        
        # Connect nodes with different actions
        self.start_node - "next" >> self.add_node1
        self.add_node1 - "next" >> self.add_node2
        
        # Create flow
        self.flow = Flow(start=self.start_node, name="test_visualization_flow")
    
    def test_generate_flow_visualization(self):
        """Test generating flow visualization HTML."""
        # Generate HTML without saving
        html = generate_flow_visualization(self.flow, title="Test Flow Visualization")
        
        # Verify HTML content contains expected elements
        self.assertIn("<title>Test Flow Visualization</title>", html)
        self.assertIn("test_visualization_flow", html)
        self.assertIn("start", html)
        self.assertIn("add_10", html)
        self.assertIn("add_20", html)
    
    def test_save_flow_visualization(self):
        """Test saving flow visualization to file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Generate output path
            output_path = os.path.join(temp_dir, "flow_visualization.html")
            
            # Generate and save visualization
            saved_path = generate_flow_visualization(
                self.flow,
                output_path=output_path,
                title="Saved Flow Visualization"
            )
            
            # Verify file was created
            self.assertEqual(saved_path, output_path)
            self.assertTrue(os.path.exists(output_path))
            
            # Verify JSON data file was also created
            json_path = output_path.replace(".html", ".json")
            self.assertTrue(os.path.exists(json_path))
            
            # Check file content
            with open(output_path, 'r') as f:
                html_content = f.read()
                self.assertIn("<title>Saved Flow Visualization</title>", html_content)
                self.assertIn("test_visualization_flow", html_content)
    
    def test_visualize_execution_path(self):
        """Test visualizing execution path through a flow."""
        # Create execution trace
        execution_trace = [
            {"node": self.start_node, "action": "next", "timestamp": "2023-01-01T00:00:00"},
            {"node": self.add_node1, "action": "next", "timestamp": "2023-01-01T00:00:01"},
            {"node": self.add_node2, "action": "next", "timestamp": "2023-01-01T00:00:02"}
        ]
        
        # Generate execution path visualization
        html = visualize_execution_path(
            self.flow,
            execution_trace,
            title="Execution Path Visualization"
        )
        
        # Verify HTML content contains execution information
        self.assertIn("<title>Execution Path Visualization</title>", html)
        self.assertIn("start", html)
        self.assertIn("add_10", html)
        self.assertIn("add_20", html)
        self.assertIn("next", html)  # Action labels
    
    def test_visualization_with_complex_flow(self):
        """Test visualization with a more complex flow structure."""
        # Create a more complex flow with branching
        start = NumberNode(10, name="start")
        
        class BranchNode(Node):
            def post(self, shared, prep_data, exec_result):
                if shared.get('current', 0) > 15:
                    return "high"
                else:
                    return "low"
        
        branch = BranchNode(name="branch")
        high_path = AddNode(100, name="high_path")
        low_path = AddNode(5, name="low_path")
        end = AddNode(0, name="end")
        
        # Connect nodes
        start - "next" >> branch
        branch - "high" >> high_path
        branch - "low" >> low_path
        high_path - "next" >> end
        low_path - "next" >> end
        
        # Create flow
        complex_flow = Flow(start=start, name="complex_flow")
        
        # Generate visualization
        html = generate_flow_visualization(complex_flow, title="Complex Flow")
        
        # Verify HTML content
        self.assertIn("complex_flow", html)
        self.assertIn("branch", html)
        self.assertIn("high_path", html)
        self.assertIn("low_path", html)
        self.assertIn("high", html)  # Action label
        self.assertIn("low", html)   # Action label


if __name__ == '__main__':
    unittest.main()