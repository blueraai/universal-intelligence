#!/usr/bin/env python3
"""
Run headless integration tests for the Universal Agents Blockly integration.
This script sets up a Node.js environment and runs the JavaScript integration tests.
"""

import os
import sys
import subprocess
import platform
import tempfile
import shutil

def check_node_installed():
    """Check if Node.js is installed."""
    try:
        result = subprocess.run(['node', '--version'], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE, 
                               check=False)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_dependencies():
    """Install required npm dependencies."""
    print("Installing test dependencies...")
    
    # Create a temporary package.json
    package_json = {
        "name": "universal-agents-blockly-tests",
        "version": "1.0.0",
        "description": "Integration tests for Universal Agents Blockly integration",
        "main": "integration_test.js",
        "dependencies": {
            "blockly": "^9.3.3",
            "jsdom": "^22.1.0"
        }
    }
    
    # Write the package.json to a temp file
    temp_dir = tempfile.mkdtemp()
    try:
        package_json_path = os.path.join(temp_dir, 'package.json')
        with open(package_json_path, 'w') as f:
            f.write("""
{
  "name": "universal-agents-blockly-tests",
  "version": "1.0.0",
  "description": "Integration tests for Universal Agents Blockly integration",
  "main": "integration_test.js",
  "dependencies": {
    "blockly": "^9.3.3",
    "jsdom": "^22.1.0"
  }
}
            """)
        
        # Run npm install
        subprocess.run(
            ['npm', 'install'], 
            cwd=temp_dir, 
            check=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        
        # Copy node_modules to current directory
        node_modules_src = os.path.join(temp_dir, 'node_modules')
        node_modules_dest = os.path.join(os.getcwd(), 'node_modules')
        
        if os.path.exists(node_modules_dest):
            shutil.rmtree(node_modules_dest)
        
        shutil.copytree(node_modules_src, node_modules_dest)
        print("Dependencies installed successfully.")
        
    except Exception as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)
    finally:
        # Clean up
        shutil.rmtree(temp_dir)

def run_tests():
    """Run the integration tests."""
    print("Running integration tests...")
    
    # Run the tests
    result = subprocess.run(
        ['node', 'integration_test.mjs'], 
        check=False
    )
    
    if result.returncode == 0:
        print("\n✅ Integration tests passed successfully!")
        return True
    else:
        print("\n❌ Integration tests failed!")
        return False

def main():
    """Main function."""
    # Check if running from the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("Universal Agents Blockly Integration Test Runner")
    print("===============================================\n")
    
    # Check if Node.js is installed
    if not check_node_installed():
        print("Error: Node.js is not installed or not in your PATH.")
        print("Please install Node.js from https://nodejs.org/")
        sys.exit(1)
    
    # Check if the integration test script exists
    if not os.path.exists('integration_test.mjs'):
        print("Error: integration_test.mjs not found in the current directory.")
        sys.exit(1)
    
    # Install dependencies if node_modules doesn't exist
    if not os.path.exists('node_modules'):
        install_dependencies()
    
    # Run the tests
    success = run_tests()
    
    # Exit with appropriate status code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()