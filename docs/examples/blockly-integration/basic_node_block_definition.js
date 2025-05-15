/**
 * Block definition for a basic Universal Agents Node.
 * This demonstrates how to create a custom Blockly block that
 * represents a Node in the Universal Agents framework.
 */

// Define the block for a Universal Agents Node
Blockly.Blocks['universal_agents_node'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Node")
        .appendField(new Blockly.FieldTextInput("MyNode"), "NODE_NAME");
    
    // Add input for the prep method
    this.appendStatementInput("PREP")
        .setCheck(null)
        .appendField("prep");
    
    // Add input for the exec method
    this.appendStatementInput("EXEC")
        .setCheck(null)
        .appendField("exec");
    
    // Add input for the post method
    this.appendStatementInput("POST")
        .setCheck(null)
        .appendField("post");
    
    // Add a value output for connecting to flows
    this.setOutput(true, "NODE");
    
    // Add action connection points
    this.appendDummyInput()
        .appendField("Actions:");
    
    this.appendValueInput("ACTION_NEXT")
        .setCheck("NODE")
        .appendField("next →");
    
    this.appendValueInput("ACTION_ERROR")
        .setCheck("NODE")
        .appendField("error →");
    
    this.appendValueInput("ACTION_CUSTOM")
        .setCheck("NODE")
        .appendField(new Blockly.FieldTextInput("custom"), "CUSTOM_ACTION")
        .appendField("→");
    
    this.setColour(230);
    this.setTooltip("Creates a Universal Agents Node with lifecycle methods");
    this.setHelpUrl("https://github.com/google/blockly");
  }
};

// Define the JavaScript generator for the Universal Agents Node block
Blockly.JavaScript['universal_agents_node'] = function(block) {
  var nodeName = block.getFieldValue('NODE_NAME');
  var prepCode = Blockly.JavaScript.statementToCode(block, 'PREP');
  var execCode = Blockly.JavaScript.statementToCode(block, 'EXEC');
  var postCode = Blockly.JavaScript.statementToCode(block, 'POST');
  
  // Get connected action nodes
  var nextNodeCode = Blockly.JavaScript.valueToCode(block, 'ACTION_NEXT', Blockly.JavaScript.ORDER_ATOMIC) || 'null';
  var errorNodeCode = Blockly.JavaScript.valueToCode(block, 'ACTION_ERROR', Blockly.JavaScript.ORDER_ATOMIC) || 'null';
  var customAction = block.getFieldValue('CUSTOM_ACTION');
  var customNodeCode = Blockly.JavaScript.valueToCode(block, 'ACTION_CUSTOM', Blockly.JavaScript.ORDER_ATOMIC) || 'null';
  
  // Generate class definition for the node
  var code = `
// Node definition
class ${nodeName} extends Node {
  constructor() {
    super("${nodeName}");
  }
  
  prep(shared) {
    ${prepCode || '    return null;'}
  }
  
  exec(prepData) {
    ${execCode || '    return prepData;'}
  }
  
  post(shared, prepData, execResult) {
    ${postCode || '    return "next";'}
  }
}

// Create instance
const ${nodeName.toLowerCase()} = new ${nodeName}();

// Connect actions
${nextNodeCode !== 'null' ? `${nodeName.toLowerCase()} - "next" >> ${nextNodeCode};` : ''}
${errorNodeCode !== 'null' ? `${nodeName.toLowerCase()} - "error" >> ${errorNodeCode};` : ''}
${customNodeCode !== 'null' ? `${nodeName.toLowerCase()} - "${customAction}" >> ${customNodeCode};` : ''}
`;

  return [nodeName.toLowerCase(), Blockly.JavaScript.ORDER_ATOMIC];
};

// Define the Python generator for the Universal Agents Node block
Blockly.Python['universal_agents_node'] = function(block) {
  var nodeName = block.getFieldValue('NODE_NAME');
  var prepCode = Blockly.Python.statementToCode(block, 'PREP');
  var execCode = Blockly.Python.statementToCode(block, 'EXEC');
  var postCode = Blockly.Python.statementToCode(block, 'POST');
  
  // Get connected action nodes
  var nextNodeCode = Blockly.Python.valueToCode(block, 'ACTION_NEXT', Blockly.Python.ORDER_ATOMIC) || 'None';
  var errorNodeCode = Blockly.Python.valueToCode(block, 'ACTION_ERROR', Blockly.Python.ORDER_ATOMIC) || 'None';
  var customAction = block.getFieldValue('CUSTOM_ACTION');
  var customNodeCode = Blockly.Python.valueToCode(block, 'ACTION_CUSTOM', Blockly.Python.ORDER_ATOMIC) || 'None';
  
  // Generate class definition for the node
  var code = `
# Node definition
class ${nodeName}(Node):
    def __init__(self):
        super().__init__("${nodeName}")
    
    def prep(self, shared):
${prepCode || '        return None'}
    
    def exec(self, prep_data):
${execCode || '        return prep_data'}
    
    def post(self, shared, prep_data, exec_result):
${postCode || '        return "next"'}

# Create instance
${nodeName.toLowerCase()} = ${nodeName}()

# Connect actions
${nextNodeCode !== 'None' ? `${nodeName.toLowerCase()} - "next" >> ${nextNodeCode}` : ''}
${errorNodeCode !== 'None' ? `${nodeName.toLowerCase()} - "error" >> ${errorNodeCode}` : ''}
${customNodeCode !== 'None' ? `${nodeName.toLowerCase()} - "${customAction}" >> ${customNodeCode}` : ''}
`;

  return [nodeName.toLowerCase(), Blockly.Python.ORDER_ATOMIC];
};