"""
Test runner for Universal Agents tests.

This module runs the Universal Agents tests with proper import mocking
to avoid dependency issues.
"""
import unittest
import sys
import os
from unittest.mock import patch

# Path setup
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Create mocks for Universal Intelligence classes
class MockAbstractUniversalModel:
    """Mock AbstractUniversalModel for testing."""
    pass

class MockAbstractUniversalTool:
    """Mock AbstractUniversalTool for testing."""
    pass

class MockAbstractUniversalAgent:
    """Mock AbstractUniversalAgent for testing."""
    pass

# Set up import mocking
core_module_mocks = {
    'universal_intelligence.core.universal_model': type('module', (), {'AbstractUniversalModel': MockAbstractUniversalModel}),
    'universal_intelligence.core.universal_tool': type('module', (), {'AbstractUniversalTool': MockAbstractUniversalTool}),
    'universal_intelligence.core.universal_agent': type('module', (), {'AbstractUniversalAgent': MockAbstractUniversalAgent}),
    'transformers': type('module', (), {'AutoModelForCausalLM': type('AutoModelForCausalLM', (), {}), 'AutoTokenizer': type('AutoTokenizer', (), {})})
}

patch_mocks = []
for module_path, mock_module in core_module_mocks.items():
    patcher = patch.dict('sys.modules', {module_path: mock_module})
    patcher.start()
    patch_mocks.append(patcher)

try:
    # Create test loader
    loader = unittest.TestLoader()
    
    # Load tests
    suite = loader.discover(os.path.dirname(__file__), pattern='test_*.py')
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with appropriate code
    sys.exit(not result.wasSuccessful())
finally:
    # Stop all patchers
    for patcher in patch_mocks:
        patcher.stop()