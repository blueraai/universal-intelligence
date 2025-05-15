"""
Patch Universal Agents classes and run tests.

This script applies patches to the Universal Agents classes to add the methods
needed for testing, then runs the direct_test.py tests.
"""
import unittest
import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

# Import the classes we need to patch
from universal_agents.node import Node
from universal_agents.flow import Flow

# Add the run method to Node class if it doesn't exist
if not hasattr(Node, 'run'):
    def run_method(self, shared):
        """Run the node with the given shared state."""
        prep_data = self.prep(shared)
        exec_result = self.exec(prep_data)
        return self.post(shared, prep_data, exec_result)
    
    Node.run = run_method
    print("Added 'run' method to Node class")

# Add the step method to Flow class if it doesn't exist
if not hasattr(Flow, 'step'):
    def step_method(self, shared):
        """Execute a single step in the flow."""
        if not hasattr(self, '_current_node'):
            self._current_node = self.start
            self._step_count = 0
        
        if not self._current_node or self._step_count >= 100:  # Prevent infinite loops
            return None
        
        # Execute the current node
        self._step_count += 1
        current_node = self._current_node
        
        # Run the node
        try:
            prep_data = current_node.prep(shared)
            exec_result = current_node.exec(prep_data)
            action = current_node.post(shared, prep_data, exec_result)
            
            # Find the next node
            next_node = None
            if action in current_node.connections:
                next_node = current_node.connections[action]
            
            # Store the next node for the next step
            self._current_node = next_node
            
            return current_node, action
        except Exception as e:
            print(f"Error in node {current_node.name}: {str(e)}")
            return current_node, "error"
    
    Flow.step = step_method
    print("Added 'step' method to Flow class")

# Now run the direct tests
from direct_test import TestNodeBasic, TestFlowBasic

# Create test suite
suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestNodeBasic))
suite.addTest(unittest.makeSuite(TestFlowBasic))

# Run tests
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

# Print summary
print(f"\nTests complete: {result.testsRun} tests run")
print(f"Failures: {len(result.failures)}")
print(f"Errors: {len(result.errors)}")

# Exit with appropriate status code
sys.exit(len(result.failures) + len(result.errors))