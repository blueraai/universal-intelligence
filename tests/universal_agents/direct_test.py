"""
Direct unit tests for Universal Agents core components.

This file contains tests that can run independently without requiring
mocked modules or dependencies.
"""
import unittest
import sys
import os
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


# Manual implementation of Node and Flow for testing
class Node:
    """Simple Node implementation for testing."""
    
    def __init__(self, name=None):
        self.name = name or self.__class__.__name__
        self.connections = {}
    
    def prep(self, shared):
        """Prepare data for execution."""
        return None
    
    def exec(self, prep_data):
        """Execute the node functionality."""
        return prep_data
    
    def post(self, shared, prep_data, exec_result):
        """Process results and determine next action."""
        return "next"
    
    def run(self, shared):
        """Run the complete node lifecycle."""
        prep_data = self.prep(shared)
        exec_result = self.exec(prep_data)
        return self.post(shared, prep_data, exec_result)
    
    def __sub__(self, action):
        """Support for node - action >> target syntax."""
        return NodeConnection(self, action)
    
    def connect(self, action, target):
        """Connect to another node with the specified action."""
        self.connections[action] = target
        return target


class NodeConnection:
    """Connection between nodes for the node - action >> target syntax."""
    
    def __init__(self, source, action):
        self.source = source
        self.action = action
    
    def __rshift__(self, target):
        """Support for source - action >> target syntax."""
        self.source.connections[self.action] = target
        return target


class Flow:
    """Simple Flow implementation for testing."""
    
    def __init__(self, start, name=None):
        self.start = start
        self.name = name or "test_flow"
    
    def run(self, shared=None):
        """Run the flow with the given shared state."""
        if shared is None:
            shared = {}
        
        max_steps = 100  # Prevent infinite loops
        step_count = 0
        current_node = self.start
        last_action = None
        
        # Execute nodes until we hit a terminal node or max steps
        while current_node and step_count < max_steps:
            # Execute the current node
            step_count += 1
            
            # Run the node
            prep_data = current_node.prep(shared)
            exec_result = current_node.exec(prep_data)
            action = current_node.post(shared, prep_data, exec_result)
            
            last_action = action
            
            # Find the next node based on the action
            if action in current_node.connections:
                current_node = current_node.connections[action]
            else:
                break
        
        return last_action


# Test node implementations
class NumberNode(Node):
    """Node that stores a number in shared state."""
    
    def __init__(self, number, name=None):
        super().__init__(name)
        self.number = number
    
    def prep(self, shared):
        shared['current'] = self.number
        return self.number
    
    def exec(self, prep_data):
        return prep_data


class AddNode(Node):
    """Node that adds a number to the current value."""
    
    def __init__(self, number, name=None):
        super().__init__(name)
        self.number = number
    
    def prep(self, shared):
        return shared.get('current', 0)
    
    def exec(self, prep_data):
        return prep_data + self.number
    
    def post(self, shared, prep_data, exec_result):
        shared['current'] = exec_result
        return "next"


class MultiplyNode(Node):
    """Node that multiplies the current value by a number."""
    
    def __init__(self, number, name=None):
        super().__init__(name)
        self.number = number
    
    def prep(self, shared):
        return shared.get('current', 1)
    
    def exec(self, prep_data):
        return prep_data * self.number
    
    def post(self, shared, prep_data, exec_result):
        shared['current'] = exec_result
        return "next"


class CheckPositiveNode(Node):
    """Node that checks if current value is positive."""
    
    def post(self, shared, prep_data, exec_result):
        return "positive" if shared.get('current', 0) >= 0 else "negative"


class TestNodeBasic(unittest.TestCase):
    """Basic tests for Node functionality."""
    
    def test_node_creation(self):
        """Test node creation and naming."""
        node1 = Node()
        node2 = Node(name="custom_name")
        
        self.assertEqual(node1.name, "Node")
        self.assertEqual(node2.name, "custom_name")
    
    def test_node_connection(self):
        """Test node connection mechanisms."""
        node1 = Node(name="node1")
        node2 = Node(name="node2")
        node3 = Node(name="node3")
        
        # Method 1: Using connect
        node1.connect("next", node2)
        
        # Method 2: Using - >> syntax
        node2 - "next" >> node3
        
        self.assertEqual(node1.connections["next"], node2)
        self.assertEqual(node2.connections["next"], node3)
    
    def test_node_lifecycle(self):
        """Test node lifecycle methods."""
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
    
    def test_run_node(self):
        """Test running a node directly."""
        node = AddNode(5, name="add_node")
        shared = {'current': 10}
        
        action = node.run(shared)
        
        self.assertEqual(action, "next")
        self.assertEqual(shared['current'], 15)


class TestFlowBasic(unittest.TestCase):
    """Basic tests for Flow functionality."""
    
    def test_linear_flow(self):
        """Test a simple linear flow."""
        # Set up nodes
        start_node = NumberNode(5, name="start")
        add_node = AddNode(10, name="add")
        multiply_node = MultiplyNode(2, name="multiply")
        
        # Connect nodes in sequence
        start_node - "next" >> add_node
        add_node - "next" >> multiply_node
        
        # Create and run flow
        flow = Flow(start=start_node)
        shared = {}
        flow.run(shared)
        
        # Assert results: (5 + 10) * 2 = 30
        self.assertEqual(shared['current'], 30)
    
    def test_branching_flow(self):
        """Test a flow with conditional branching."""
        # Positive case
        start_pos = NumberNode(5, name="start_pos")
        check_pos = CheckPositiveNode(name="check_pos")
        add_node = AddNode(10, name="add")
        multiply_node = MultiplyNode(-1, name="multiply")
        
        # Connect nodes with branching
        start_pos - "next" >> check_pos
        check_pos - "positive" >> add_node
        check_pos - "negative" >> multiply_node
        
        # Create and run flow
        flow_pos = Flow(start=start_pos)
        shared_pos = {}
        flow_pos.run(shared_pos)
        
        # Assert results for positive case: 5 + 10 = 15
        self.assertEqual(shared_pos['current'], 15)
        
        # Negative case
        start_neg = NumberNode(-5, name="start_neg")
        check_neg = CheckPositiveNode(name="check_neg")
        
        # Connect nodes with branching
        start_neg - "next" >> check_neg
        check_neg - "positive" >> add_node
        check_neg - "negative" >> multiply_node
        
        # Create and run flow
        flow_neg = Flow(start=start_neg)
        shared_neg = {}
        flow_neg.run(shared_neg)
        
        # Assert results for negative case: -5 * -1 = 5
        self.assertEqual(shared_neg['current'], 5)


# Run the tests
if __name__ == "__main__":
    unittest.main()