# Universal Agents Blockly Integration Example

This directory contains example files demonstrating how to integrate Google's Blockly visual programming editor with the Universal Agents framework.

## Overview

The Universal Agents Blockly integration allows users to create, visualize, and execute Universal Agents workflows using a drag-and-drop interface. This makes the framework more accessible to users with limited programming experience while maintaining the full power and flexibility of Universal Agents.

## Example Files

This directory includes:

1. **index.html** - Main HTML file with the Blockly interface and code preview panels
2. **basic_node_block_definition.js** - Definition of a basic Universal Agents Node block
3. **flow_block_definition.js** - Definition of a Universal Agents Flow block
4. **model_node_block_definition.js** - Definition of a Universal Model Node block
5. **toolbox_configuration.js** - Configuration of the Blockly toolbox with categories and blocks
6. **test.js** - Integration tests to verify the Blockly integration functionality
7. **server.py** - Simple HTTP server for running the demo

## How to Run the Example

### Method 1: Using the Python Server (Recommended)

1. Navigate to this directory:
   ```bash
   cd docs/examples/blockly-integration
   ```

2. Make the server script executable:
   ```bash
   chmod +x server.py
   ```

3. Run the server:
   ```bash
   python3 server.py
   ```

4. Open your browser and navigate to:
   ```
   http://localhost:8000/index.html
   ```

### Method 2: Using a Different HTTP Server

You can use any HTTP server to serve the files in this directory:

1. Using Python's built-in HTTP server:
   ```bash
   cd docs/examples/blockly-integration
   python3 -m http.server 8000
   ```

2. Using Node.js and http-server:
   ```bash
   cd docs/examples/blockly-integration
   npx http-server -p 8000
   ```

### After Opening the Example

1. Try building a simple flow by dragging blocks from the toolbox
2. The generated code will appear in the right panel
3. You can switch between JavaScript and Python code views
4. Use the buttons to save, load, export, or run your flow
5. Click "Run Tests" to check if the integration is working correctly

## Troubleshooting

If you encounter issues with the demo:

1. **Browser Console Errors**: Open your browser's developer tools (F12 or Ctrl+Shift+I) and check the console for errors.

2. **CORS Issues**: If you see errors related to CORS, make sure you're using the provided server.py which handles CORS headers.

3. **Block Loading Problems**: Ensure all the JavaScript files are being loaded correctly. Check the network tab in developer tools.

4. **Running Tests**: The "Run Tests" button runs integration tests that can help diagnose issues. If tests fail, the error messages will indicate what's not working.

5. **Clearing Cache**: Try clearing your browser cache if you've made changes that aren't showing up.

## Block Types

The example includes several types of blocks:

### Core Blocks

- **Node** - Basic Universal Agents Node with prep, exec, and post methods
- **Flow** - Universal Agents Flow with start node and visualization options

### Universal Integration Blocks

- **ModelNode** - Node for using Universal Intelligence models
- **ToolNode** - Node for using Universal Intelligence tools (not shown in example files)
- **AgentNode** - Node for using Universal Intelligence agents (not shown in example files)

### Pattern Blocks

The toolbox configuration includes placeholders for pattern blocks like RAG, Map-Reduce, Multi-Agent, and Workflow patterns.

## Extending the Example

To extend this example:

1. Create new block definitions by following the pattern in the existing files
2. Add them to the toolbox configuration
3. Implement code generators for JavaScript and Python
4. Include your new block definition files in index.html

## Future Work

This example demonstrates the basic concepts and structure for a Blockly integration. A complete implementation would include:

1. More block types covering all Universal Agents features
2. Advanced code generation with proper imports and dependencies
3. Full flow visualization and execution
4. Improved UI with better error handling and feedback
5. Integration with the Universal Agents runtime for direct execution

## References

- [Blockly Documentation](https://developers.google.com/blockly/guides/overview)
- [Universal Agents Documentation](../../guides/guide-universal-agents-usage-v1.0.0.md)
- [Blockly Integration Analysis](../../analysis/blockly-integration-analysis.md)
- [Blockly Integration Plan](../../plans/plan-blockly-integration-v1.0.0.md)