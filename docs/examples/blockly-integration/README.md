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

## How to Run the Example

1. Make sure you have a local web server running
2. Open `index.html` in a web browser
3. Try building a simple flow by dragging blocks from the toolbox
4. The generated code will appear in the right panel
5. You can switch between JavaScript and Python code views
6. Use the buttons to save, load, export, or run your flow

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