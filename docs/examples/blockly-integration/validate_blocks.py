#!/usr/bin/env python3
"""
Simple validation script for Universal Agents Blockly integration.
This script checks that all the necessary block definition files exist
and have the required components.
"""

import os
import sys
import re
import json

def validate_file_exists(file_path, description):
    """Check if a file exists and is not empty."""
    if not os.path.exists(file_path):
        print(f"❌ {description} file not found: {file_path}")
        return False
    
    if os.path.getsize(file_path) == 0:
        print(f"❌ {description} file is empty: {file_path}")
        return False
    
    print(f"✓ {description} file exists and is not empty")
    return True

def validate_js_content(file_path, required_patterns):
    """Check if a JavaScript file contains required patterns."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        for pattern, description in required_patterns:
            if not re.search(pattern, content, re.DOTALL):
                print(f"❌ Missing {description} in {os.path.basename(file_path)}")
                return False
            print(f"✓ Found {description} in {os.path.basename(file_path)}")
        
        return True
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return False

def validate_html_content(file_path, required_patterns):
    """Check if an HTML file contains required patterns."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        for pattern, description in required_patterns:
            if not re.search(pattern, content, re.DOTALL):
                print(f"❌ Missing {description} in {os.path.basename(file_path)}")
                return False
            print(f"✓ Found {description} in {os.path.basename(file_path)}")
        
        return True
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return False

def validate_basic_node_block():
    """Validate the basic node block definition."""
    file_path = 'basic_node_block_definition.js'
    
    if not validate_file_exists(file_path, "Basic node block definition"):
        return False
    
    required_patterns = [
        (r"Blockly\.Blocks\['universal_agents_node'\]", "Block definition"),
        (r"init:\s*function\(\)", "Init function"),
        (r"Blockly\.JavaScript\['universal_agents_node'\]", "JavaScript generator"),
        (r"Blockly\.Python\['universal_agents_node'\]", "Python generator"),
    ]
    
    return validate_js_content(file_path, required_patterns)

def validate_flow_block():
    """Validate the flow block definition."""
    file_path = 'flow_block_definition.js'
    
    if not validate_file_exists(file_path, "Flow block definition"):
        return False
    
    required_patterns = [
        (r"Blockly\.Blocks\['universal_agents_flow'\]", "Block definition"),
        (r"init:\s*function\(\)", "Init function"),
        (r"Blockly\.JavaScript\['universal_agents_flow'\]", "JavaScript generator"),
        (r"Blockly\.Python\['universal_agents_flow'\]", "Python generator"),
    ]
    
    return validate_js_content(file_path, required_patterns)

def validate_model_node_block():
    """Validate the model node block definition."""
    file_path = 'model_node_block_definition.js'
    
    if not validate_file_exists(file_path, "Model node block definition"):
        return False
    
    required_patterns = [
        (r"Blockly\.Blocks\['universal_model_node'\]", "Block definition"),
        (r"init:\s*function\(\)", "Init function"),
        (r"Blockly\.JavaScript\['universal_model_node'\]", "JavaScript generator"),
        (r"Blockly\.Python\['universal_model_node'\]", "Python generator"),
    ]
    
    return validate_js_content(file_path, required_patterns)

def validate_toolbox_config():
    """Validate the toolbox configuration."""
    file_path = 'toolbox_configuration.js'
    
    if not validate_file_exists(file_path, "Toolbox configuration"):
        return False
    
    required_patterns = [
        (r"var\s+toolboxConfig", "Toolbox configuration variable"),
        (r"\"kind\":\s*\"categoryToolbox\"", "Category toolbox kind"),
        (r"\"universal_agents_node\"", "Universal agents node block reference"),
        (r"\"universal_agents_flow\"", "Universal agents flow block reference"),
        (r"\"universal_model_node\"", "Universal model node block reference"),
    ]
    
    return validate_js_content(file_path, required_patterns)

def validate_index_html():
    """Validate the index HTML file."""
    file_path = 'index.html'
    
    if not validate_file_exists(file_path, "Index HTML"):
        return False
    
    required_patterns = [
        (r"<script\s+src=\"basic_node_block_definition\.js\"", "Basic node block script include"),
        (r"<script\s+src=\"flow_block_definition\.js\"", "Flow block script include"),
        (r"<script\s+src=\"model_node_block_definition\.js\"", "Model node block script include"),
        (r"<script\s+src=\"toolbox_configuration\.js\"", "Toolbox configuration script include"),
        (r"<div\s+id=\"blocklyDiv\"", "Blockly div container"),
    ]
    
    return validate_html_content(file_path, required_patterns)

def validate_server_script():
    """Validate the server script."""
    file_path = 'server.py'
    
    if not validate_file_exists(file_path, "Server script"):
        return False
    
    # Server script exists and is not empty, that's enough for validation
    return True

def validate_test_script():
    """Validate the test script."""
    file_path = 'test.js'
    
    if not validate_file_exists(file_path, "Test script"):
        return False
    
    required_patterns = [
        (r"function\s+runBlocklyIntegrationTests", "Integration tests function"),
        (r"displayTestResults", "Test results display function"),
    ]
    
    return validate_js_content(file_path, required_patterns)

def main():
    """Main entry point."""
    print("Universal Agents Blockly Integration Validation")
    print("===============================================\n")
    
    # Change to the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Run validations
    results = []
    results.append(validate_basic_node_block())
    results.append(validate_flow_block())
    results.append(validate_model_node_block())
    results.append(validate_toolbox_config())
    results.append(validate_index_html())
    results.append(validate_server_script())
    results.append(validate_test_script())
    
    # Print summary
    passed = sum(1 for r in results if r)
    failed = sum(1 for r in results if not r)
    
    print("\nValidation Summary")
    print("-----------------")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    # Return success if all validations passed
    return 0 if all(results) else 1

if __name__ == "__main__":
    sys.exit(main())