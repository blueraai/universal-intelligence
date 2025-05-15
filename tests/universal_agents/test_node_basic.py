"""
Tests for the basic Node functionality in Universal Agents.
"""
import unittest
import sys
from pathlib import Path
import warnings

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from universal_agents.node import Node


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


class MultiplyNode(Node):
    """A node that multiplies the current value in shared state by a number."""
    def __init__(self, number, name=None):
        super().__init__(name=name)
        self.number = number
    
    def prep(self, shared):
        if 'current' not in shared:
            shared['current'] = 1
        return shared['current']
    
    def exec(self, prep_data):
        return prep_data * self.number
    
    def post(self, shared, prep_data, exec_result):
        shared['current'] = exec_result
        return "next"


class CheckPositiveNode(Node):
    """A node that checks if the current value is positive and branches accordingly."""
    def __init__(self, name=None):
        super().__init__(name=name)
    
    def prep(self, shared):
        if 'current' not in shared:
            shared['current'] = 0
        return shared['current']
    
    def exec(self, prep_data):
        return prep_data >= 0
    
    def post(self, shared, prep_data, exec_result):
        return "positive" if exec_result else "negative"


class EndSignalNode(Node):
    """A node that returns a specific signal to stop the flow."""
    def __init__(self, signal="complete", name=None):
        super().__init__(name=name)
        self.signal = signal
    
    def post(self, shared, prep_data, exec_result):
        return self.signal


class TestNodeBasic(unittest.TestCase):
    
    def test_node_lifecycle(self):
        """Test the full prep/exec/post lifecycle of a node."""
        node = AddNode(5, name="add_node")
        shared = {'current': 10}
        
        # Test prep
        prep_data = node.prep(shared)
        self.assertEqual(prep_data, 10)
        
        # Test exec
        exec_result = node.exec(prep_data)
        self.assertEqual(exec_result, 15)
        
        # Test post
        action = node.post(shared, prep_data, exec_result)
        self.assertEqual(action, "next")
        self.assertEqual(shared['current'], 15)
    
    def test_node_connection(self):
        """Test node connection mechanisms."""
        start_node = NumberNode(5, name="start")
        add_node = AddNode(10, name="add")
        multiply_node = MultiplyNode(2, name="multiply")
        
        # Connect nodes using the - >> syntax
        start_node - "next" >> add_node
        add_node - "next" >> multiply_node
        
        # Verify connections
        self.assertIn("next", start_node.connections)
        self.assertEqual(start_node.connections["next"], add_node)
        self.assertIn("next", add_node.connections)
        self.assertEqual(add_node.connections["next"], multiply_node)
    
    def test_conditional_branching(self):
        """Test conditional branching in nodes."""
        check_node = CheckPositiveNode(name="check")
        positive_node = AddNode(10, name="positive_branch")
        negative_node = MultiplyNode(-1, name="negative_branch")
        
        # Set up conditional branches
        check_node - "positive" >> positive_node
        check_node - "negative" >> negative_node
        
        # Verify connections
        self.assertIn("positive", check_node.connections)
        self.assertEqual(check_node.connections["positive"], positive_node)
        self.assertIn("negative", check_node.connections)
        self.assertEqual(check_node.connections["negative"], negative_node)
        
        # Test positive case
        shared = {'current': 5}
        prep_data = check_node.prep(shared)
        exec_result = check_node.exec(prep_data)
        action = check_node.post(shared, prep_data, exec_result)
        self.assertEqual(action, "positive")
        
        # Test negative case
        shared = {'current': -5}
        prep_data = check_node.prep(shared)
        exec_result = check_node.exec(prep_data)
        action = check_node.post(shared, prep_data, exec_result)
        self.assertEqual(action, "negative")
    
    def test_node_name(self):
        """Test node naming functionality."""
        # Node with explicit name
        named_node = NumberNode(5, name="explicit_name")
        self.assertEqual(named_node.name, "explicit_name")
        
        # Node with default name (class name)
        default_named_node = NumberNode(5)
        self.assertEqual(default_named_node.name, "NumberNode")
    
    def test_run_node(self):
        """Test running a node directly with the run method."""
        node = AddNode(5, name="add_node")
        shared = {'current': 10}
        
        action = node.run(shared)
        
        self.assertEqual(action, "next")
        self.assertEqual(shared['current'], 15)


if __name__ == '__main__':
    unittest.main()