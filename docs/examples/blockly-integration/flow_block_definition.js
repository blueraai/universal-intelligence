/**
 * Block definition for a Universal Agents Flow.
 * This demonstrates how to create a custom Blockly block that
 * represents a Flow in the Universal Agents framework.
 */

// For Blockly v12, we need to register generators properly
if (!Blockly.JavaScript) {
  Blockly.JavaScript = new Blockly.Generator('JavaScript');
}
if (!Blockly.Python) {
  Blockly.Python = new Blockly.Generator('Python');
}

// Define the block for a Universal Agents Flow
Blockly.Blocks['universal_agents_flow'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Flow")
        .appendField(new Blockly.FieldTextInput("MyFlow"), "FLOW_NAME");
    
    // Add input for the starting node
    this.appendValueInput("START_NODE")
        .setCheck("NODE")
        .appendField("start");
    
    // Add checkbox for visualization
    this.appendDummyInput()
        .appendField("visualization")
        .appendField(new Blockly.FieldCheckbox("FALSE"), "VISUALIZATION");
    
    // Add input for visualization path (optional)
    this.appendDummyInput()
        .appendField("path")
        .appendField(new Blockly.FieldTextInput("visualizations"), "VIZ_PATH");
    
    // Add a value output to allow this flow to be referenced
    this.setOutput(true, "FLOW");
    
    // Set the appearance of the block
    this.setColour(160);
    this.setTooltip("Creates a Universal Agents Flow with the specified start node");
    this.setHelpUrl("https://github.com/google/blockly");
  }
};

// Define the JavaScript generator for the Universal Agents Flow block
Blockly.JavaScript['universal_agents_flow'] = function(block) {
  var flowName = block.getFieldValue('FLOW_NAME');
  var startNodeCode = Blockly.JavaScript.valueToCode(block, 'START_NODE', Blockly.JavaScript.ORDER_ATOMIC) || 'null';
  var visualization = block.getFieldValue('VISUALIZATION') === 'TRUE';
  var vizPath = block.getFieldValue('VIZ_PATH');
  
  // Generate flow initialization and execution code
  var code = `
// Flow definition
const ${flowName.toLowerCase()} = new Flow(
  start=${startNodeCode},
  name="${flowName}"${visualization ? `,
  visualization=true,
  visualization_path="${vizPath}"` : ''}
);

// Initialize shared state
const shared = {};

// Run the flow
const result = ${flowName.toLowerCase()}.run(shared);
`;

  return [flowName.toLowerCase(), Blockly.JavaScript.ORDER_ATOMIC];
};

// Define the Python generator for the Universal Agents Flow block
Blockly.Python['universal_agents_flow'] = function(block) {
  var flowName = block.getFieldValue('FLOW_NAME');
  var startNodeCode = Blockly.Python.valueToCode(block, 'START_NODE', Blockly.Python.ORDER_ATOMIC) || 'None';
  var visualization = block.getFieldValue('VISUALIZATION') === 'TRUE';
  var vizPath = block.getFieldValue('VIZ_PATH');
  
  // Generate flow initialization and execution code
  var code = `
# Flow definition
${flowName.toLowerCase()} = Flow(
    start=${startNodeCode},
    name="${flowName}"${visualization ? `,
    visualization=True,
    visualization_path="${vizPath}"` : ''}
)

# Initialize shared state
shared = {}

# Run the flow
result = ${flowName.toLowerCase()}.run(shared)
`;

  return [flowName.toLowerCase(), Blockly.Python.ORDER_ATOMIC];
};