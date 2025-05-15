"""
Tests for the basic Flow functionality in Universal Agents.
"""
import unittest
import sys
from pathlib import Path
import warnings

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from universal_agents.node import Node
from universal_agents.flow import Flow


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


class TestFlowBasic(unittest.TestCase):
    
    def test_linear_flow(self):
        """Test a simple linear flow with three nodes."""
        # Create nodes
        start_node = NumberNode(5, name="start")
        add_node = AddNode(10, name="add")
        multiply_node = MultiplyNode(2, name="multiply")
        
        # Connect nodes
        start_node - "next" >> add_node
        add_node - "next" >> multiply_node
        
        # Create flow
        flow = Flow(start=start_node, name="linear_flow")
        
        # Run flow
        shared = {}
        result = flow.run(shared)
        
        # Verify result
        self.assertEqual(shared['current'], 30)  # (5 + 10) * 2
        self.assertEqual(result, "next")  # Last action from multiply_node
    
    def test_branching_flow_positive(self):
        """Test a flow with conditional branching (positive path)."""
        # Create nodes
        start_node = NumberNode(5, name="start")
        check_node = CheckPositiveNode(name="check")
        positive_node = AddNode(10, name="positive_branch")
        negative_node = MultiplyNode(-1, name="negative_branch")
        
        # Connect nodes
        start_node - "next" >> check_node
        check_node - "positive" >> positive_node
        check_node - "negative" >> negative_node
        
        # Create flow
        flow = Flow(start=start_node, name="branch_flow")
        
        # Run flow
        shared = {}
        result = flow.run(shared)
        
        # Verify result
        self.assertEqual(shared['current'], 15)  # 5 + 10 (positive branch)
        self.assertEqual(result, "next")  # Last action from positive_node
    
    def test_branching_flow_negative(self):
        """Test a flow with conditional branching (negative path)."""
        # Create nodes
        start_node = NumberNode(-5, name="start")
        check_node = CheckPositiveNode(name="check")
        positive_node = AddNode(10, name="positive_branch")
        negative_node = MultiplyNode(-1, name="negative_branch")
        
        # Connect nodes
        start_node - "next" >> check_node
        check_node - "positive" >> positive_node
        check_node - "negative" >> negative_node
        
        # Create flow
        flow = Flow(start=start_node, name="branch_flow")
        
        # Run flow
        shared = {}
        result = flow.run(shared)
        
        # Verify result
        self.assertEqual(shared['current'], 5)  # -5 * -1 (negative branch)
        self.assertEqual(result, "next")  # Last action from negative_node
    
    def test_flow_with_end_signal(self):
        """Test a flow that ends with a specific signal."""
        # Create nodes
        start_node = NumberNode(5, name="start")
        add_node = AddNode(10, name="add")
        end_node = EndSignalNode(signal="flow_complete", name="end")
        
        # Connect nodes
        start_node - "next" >> add_node
        add_node - "next" >> end_node
        
        # Create flow
        flow = Flow(start=start_node, name="signal_flow")
        
        # Run flow
        shared = {}
        result = flow.run(shared)
        
        # Verify result
        self.assertEqual(shared['current'], 15)  # 5 + 10
        self.assertEqual(result, "flow_complete")  # Signal from end_node
    
    def test_cyclic_flow(self):
        """Test a flow with a cycle that terminates after a condition is met."""
        # Create nodes
        start_node = NumberNode(10, name="start")
        check_node = CheckPositiveNode(name="check")
        subtract_node = AddNode(-3, name="subtract")
        end_node = EndSignalNode(signal="cycle_complete", name="end")
        
        # Connect nodes to create a cycle
        start_node - "next" >> check_node
        check_node - "positive" >> subtract_node
        check_node - "negative" >> end_node
        subtract_node - "next" >> check_node  # Cycle back to check
        
        # Create flow
        flow = Flow(start=start_node, name="cyclic_flow")
        
        # Run flow
        shared = {}
        result = flow.run(shared)
        
        # Verify result: 10 -> 7 -> 4 -> 1 -> -2 (now negative) -> end
        self.assertEqual(shared['current'], -2)
        self.assertEqual(result, "cycle_complete")
    
    def test_flow_with_missing_connection(self):
        """Test flow behavior when a node's output action has no matching connection."""
        # Create nodes
        start_node = NumberNode(5, name="start")
        check_node = CheckPositiveNode(name="check")
        
        # Connect only the positive path
        start_node - "next" >> check_node
        check_node - "positive" >> AddNode(10, name="positive_branch")
        # No connection for "negative" action
        
        # Create flow
        flow = Flow(start=start_node, name="incomplete_flow")
        
        # Run flow with negative value to trigger missing connection
        shared = {'current': -5}  # Override start_node's value
        
        # Capture the warning
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = flow.run(shared)
            
            # Verify a warning was raised
            self.assertGreaterEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, UserWarning))
            self.assertIn("negative", str(w[0].message))
    
    def test_step_by_step_execution(self):
        """Test step-by-step execution of a flow."""
        # Create nodes
        start_node = NumberNode(5, name="start")
        add_node = AddNode(10, name="add")
        multiply_node = MultiplyNode(2, name="multiply")
        
        # Connect nodes
        start_node - "next" >> add_node
        add_node - "next" >> multiply_node
        
        # Create flow
        flow = Flow(start=start_node, name="step_flow")
        
        # Run flow step by step
        shared = {}
        steps = []
        
        step_result = flow.step(shared)
        steps.append((step_result[0].name, shared.get('current')))
        
        step_result = flow.step(shared)
        steps.append((step_result[0].name, shared.get('current')))
        
        step_result = flow.step(shared)
        steps.append((step_result[0].name, shared.get('current')))
        
        # No more steps
        step_result = flow.step(shared)
        self.assertIsNone(step_result)
        
        # Verify execution steps
        self.assertEqual(steps, [
            ('start', 5),     # After NumberNode
            ('add', 15),      # After AddNode
            ('multiply', 30)  # After MultiplyNode
        ])


if __name__ == '__main__':
    unittest.main()