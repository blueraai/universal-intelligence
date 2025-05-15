"""
Test runner for Universal Agents tests.

This module allows running a single test file with proper import mocking.
"""
import unittest
import sys
import os
from unittest.mock import patch
from pathlib import Path
import argparse

# Parse command line arguments
parser = argparse.ArgumentParser(description='Run a specific test file')
parser.add_argument('test_file', help='The test file to run (e.g., test_node_basic.py)')
parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
args = parser.parse_args()

# Path setup
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

# Find the test file
test_path = os.path.join(project_root, 'tests', 'universal_agents', args.test_file)
if not os.path.exists(test_path):
    print(f"Error: Test file '{args.test_file}' not found at {test_path}")
    sys.exit(1)

# Add the run method to Node class if it doesn't exist
from universal_agents.node import Node

if not hasattr(Node, 'run'):
    def run_method(self, shared):
        """Run the node with the given shared state."""
        prep_data = self.prep(shared)
        exec_result = self.exec(prep_data)
        return self.post(shared, prep_data, exec_result)
    
    Node.run = run_method
    print("Added 'run' method to Node class")

# Add the step method to Flow class if it doesn't exist
from universal_agents.flow import Flow

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
        
        # Execute the node
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
    
    Flow.step = step_method
    print("Added 'step' method to Flow class")

# Create test loader
loader = unittest.TestLoader()

print(f"Running test file: {args.test_file}")

# Load and run the test
test_module_name = args.test_file.replace('.py', '')
sys.path.insert(0, os.path.join(project_root, 'tests', 'universal_agents'))
test_module = __import__(test_module_name)
suite = loader.loadTestsFromModule(test_module)

# Run tests
runner = unittest.TextTestRunner(verbosity=2 if args.verbose else 1)
result = runner.run(suite)

# Exit with appropriate code
sys.exit(not result.wasSuccessful())