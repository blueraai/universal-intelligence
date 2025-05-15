#!/usr/bin/env python3
"""
Launcher script for the Universal Agents Blockly integration demo.

This script automatically finds and runs the Blockly integration demo server
or the integration tests, depending on the command-line arguments.
"""

import os
import sys
import subprocess
import argparse

def find_demo_directory():
    """Find the Blockly integration demo directory."""
    # Possible locations for the demo
    possible_paths = [
        "docs/examples/blockly-integration",
        "docs/examples/blockly_integration",
        "examples/blockly-integration",
        "examples/blockly_integration"
    ]
    
    # Start from the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check each possible path
    for path in possible_paths:
        full_path = os.path.join(script_dir, path)
        if os.path.exists(full_path) and os.path.exists(os.path.join(full_path, "index.html")):
            return full_path
    
    return None

def run_server(demo_dir):
    """Run the demo server."""
    # Find the server script
    server_script = os.path.join(demo_dir, "server.py")
    
    if not os.path.exists(server_script):
        print(f"ERROR: Server script not found at {server_script}")
        return 1
    
    # Make the script executable
    try:
        os.chmod(server_script, 0o755)
    except Exception as e:
        print(f"WARNING: Could not make server script executable: {e}")
    
    # Run the server
    print(f"Starting Blockly demo server from: {demo_dir}")
    try:
        # Change to the demo directory
        os.chdir(demo_dir)
        
        # Run the server script
        subprocess.call([sys.executable, server_script])
        return 0
    except Exception as e:
        print(f"ERROR: Failed to run the demo server: {e}")
        return 1

def run_tests(demo_dir):
    """Run the integration tests."""
    # Find the validation script
    validation_script = os.path.join(demo_dir, "validate_blocks.py")
    
    if not os.path.exists(validation_script):
        print(f"ERROR: Validation script not found at {validation_script}")
        return 1
    
    # Make the script executable
    try:
        os.chmod(validation_script, 0o755)
    except Exception as e:
        print(f"WARNING: Could not make validation script executable: {e}")
    
    # Run the tests
    print(f"Running Blockly validation tests from: {demo_dir}")
    try:
        # Change to the demo directory
        os.chdir(demo_dir)
        
        # Run the validation script
        result = subprocess.call([sys.executable, validation_script])
        return result
    except Exception as e:
        print(f"ERROR: Failed to run the validation tests: {e}")
        return 1

def main():
    """Main entry point."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Universal Agents Blockly integration tools')
    parser.add_argument('--tests', action='store_true', help='Run integration tests instead of starting the demo server')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode (for CI/CD)')
    args = parser.parse_args()
    
    # Find the demo directory
    demo_dir = find_demo_directory()
    
    if not demo_dir:
        print("ERROR: Could not find the Blockly integration demo directory.")
        print("Make sure you have the demo files in one of these locations:")
        print("  - docs/examples/blockly-integration")
        print("  - docs/examples/blockly_integration")
        print("  - examples/blockly-integration")
        print("  - examples/blockly_integration")
        return 1
    
    # Run tests or server
    if args.tests:
        return run_tests(demo_dir)
    else:
        return run_server(demo_dir)

if __name__ == "__main__":
    sys.exit(main())