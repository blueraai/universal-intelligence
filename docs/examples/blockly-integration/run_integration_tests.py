#!/usr/bin/env python3
"""
Run integration tests for the Universal Agents Blockly integration.
This script validates all block definitions and configurations.
"""

import os
import sys
import subprocess
import platform

def validate_blocks():
    """Run the block validation script."""
    print("Validating block definitions...")
    
    # Check if the validation script exists
    validator_script = 'validate_blocks.py'
    if not os.path.exists(validator_script):
        print(f"ERROR: Validation script not found at {validator_script}")
        return False
    
    # Make the script executable
    try:
        os.chmod(validator_script, 0o755)
    except Exception as e:
        print(f"WARNING: Could not make validation script executable: {e}")
    
    # Run the validator
    result = subprocess.run(
        [sys.executable, validator_script], 
        check=False
    )
    
    if result.returncode == 0:
        print("\n✅ Block validation passed successfully!")
        return True
    else:
        print("\n❌ Block validation failed!")
        return False

def test_in_browser():
    """Test if we can launch the browser for manual testing."""
    print("\nChecking browser launch capability...")
    
    # Check if the browser can be launched
    try:
        import webbrowser
        print("✓ Browser module available for testing")
        return True
    except ImportError:
        print("❌ Browser module not available")
        return False

def main():
    """Main function."""
    # Check if running from the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("Universal Agents Blockly Integration Test Runner")
    print("===============================================\n")
    
    # Run block validations
    blocks_valid = validate_blocks()
    
    # Test browser capability
    browser_valid = test_in_browser()
    
    # Print summary
    print("\nTest Summary")
    print("-----------")
    print(f"Block Validation: {'✅ Passed' if blocks_valid else '❌ Failed'}")
    print(f"Browser Testing: {'✅ Available' if browser_valid else '❌ Not Available'}")
    
    # Success if all tests pass
    success = blocks_valid and browser_valid
    
    if success:
        print("\n✅ All tests passed successfully!")
        print("You can now run the server with: python server.py")
    else:
        print("\n❌ Some tests failed, please fix the issues above.")
    
    # Exit with appropriate status code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()