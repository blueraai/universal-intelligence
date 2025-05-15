/**
 * Block definition for a Universal Agents ModelNode.
 * This demonstrates how to create a custom Blockly block that
 * represents a Universal Intelligence Model Node in the Universal Agents framework.
 */

// Define the block for a Universal Model Node
Blockly.Blocks['universal_model_node'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("ModelNode")
        .appendField(new Blockly.FieldTextInput("MyModelNode"), "NODE_NAME");
    
    // Add model selection dropdown
    // In a real implementation, this would be populated with available models
    this.appendDummyInput()
        .appendField("model")
        .appendField(new Blockly.FieldDropdown([
          ["Default", "UniversalModel()"],
          ["Llama3-8B", "Llama3Model()"],
          ["Qwen2-7B", "Qwen2Model()"],
          ["CustomModel", "CustomModel()"]
        ]), "MODEL");
    
    // Add prompt template input
    this.appendDummyInput()
        .appendField("prompt template:");
    this.appendDummyInput()
        .appendField(new Blockly.FieldMultilineInput("Please answer the following question:\n\nQuestion: {question}\n\nAnswer:"), "PROMPT_TEMPLATE");
    
    // Add input keys
    this.appendDummyInput()
        .appendField("input keys:")
        .appendField(new Blockly.FieldTextInput("question"), "INPUT_KEYS");
    
    // Add output key
    this.appendDummyInput()
        .appendField("output key:")
        .appendField(new Blockly.FieldTextInput("answer"), "OUTPUT_KEY");
    
    // Add parameters
    this.appendDummyInput()
        .appendField("parameters:");
    this.appendDummyInput()
        .appendField("temperature:")
        .appendField(new Blockly.FieldNumber(0.7, 0, 2, 0.1), "TEMPERATURE");
    this.appendDummyInput()
        .appendField("max tokens:")
        .appendField(new Blockly.FieldNumber(1000, 0, 10000, 1), "MAX_TOKENS");
    
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
    
    // Set the appearance of the block
    this.setColour(290);
    this.setTooltip("Creates a Universal Model Node for using language models");
    this.setHelpUrl("https://github.com/google/blockly");
  }
};

// Define the JavaScript generator for the Universal Model Node block
Blockly.JavaScript['universal_model_node'] = function(block) {
  var nodeName = block.getFieldValue('NODE_NAME');
  var model = block.getFieldValue('MODEL');
  var promptTemplate = block.getFieldValue('PROMPT_TEMPLATE');
  var inputKeys = block.getFieldValue('INPUT_KEYS').split(',').map(k => k.trim());
  var outputKey = block.getFieldValue('OUTPUT_KEY');
  var temperature = block.getFieldValue('TEMPERATURE');
  var maxTokens = block.getFieldValue('MAX_TOKENS');
  
  // Get connected action nodes
  var nextNodeCode = Blockly.JavaScript.valueToCode(block, 'ACTION_NEXT', Blockly.JavaScript.ORDER_ATOMIC) || 'null';
  var errorNodeCode = Blockly.JavaScript.valueToCode(block, 'ACTION_ERROR', Blockly.JavaScript.ORDER_ATOMIC) || 'null';
  
  // Generate node initialization code
  var code = `
// Model node initialization
const ${nodeName.toLowerCase()} = new UniversalModelNode(
  model: ${model},
  prompt_template: \`${promptTemplate}\`,
  input_keys: [${inputKeys.map(k => `"${k}"`).join(', ')}],
  output_key: "${outputKey}",
  name: "${nodeName}",
  model_parameters: {
    temperature: ${temperature},
    max_tokens: ${maxTokens}
  }
);

// Connect actions
${nextNodeCode !== 'null' ? `${nodeName.toLowerCase()} - "next" >> ${nextNodeCode};` : ''}
${errorNodeCode !== 'null' ? `${nodeName.toLowerCase()} - "error" >> ${errorNodeCode};` : ''}
`;

  return [nodeName.toLowerCase(), Blockly.JavaScript.ORDER_ATOMIC];
};

// Define the Python generator for the Universal Model Node block
Blockly.Python['universal_model_node'] = function(block) {
  var nodeName = block.getFieldValue('NODE_NAME');
  var model = block.getFieldValue('MODEL');
  var promptTemplate = block.getFieldValue('PROMPT_TEMPLATE');
  var inputKeys = block.getFieldValue('INPUT_KEYS').split(',').map(k => k.trim());
  var outputKey = block.getFieldValue('OUTPUT_KEY');
  var temperature = block.getFieldValue('TEMPERATURE');
  var maxTokens = block.getFieldValue('MAX_TOKENS');
  
  // Get connected action nodes
  var nextNodeCode = Blockly.Python.valueToCode(block, 'ACTION_NEXT', Blockly.Python.ORDER_ATOMIC) || 'None';
  var errorNodeCode = Blockly.Python.valueToCode(block, 'ACTION_ERROR', Blockly.Python.ORDER_ATOMIC) || 'None';
  
  // Generate node initialization code
  var code = `
# Model node initialization
${nodeName.toLowerCase()} = UniversalModelNode(
    model=${model},
    prompt_template="""${promptTemplate}""",
    input_keys=[${inputKeys.map(k => `"${k}"`).join(', ')}],
    output_key="${outputKey}",
    name="${nodeName}",
    model_parameters={
        "temperature": ${temperature},
        "max_tokens": ${maxTokens}
    }
)

# Connect actions
${nextNodeCode !== 'None' ? `${nodeName.toLowerCase()} - "next" >> ${nextNodeCode}` : ''}
${errorNodeCode !== 'None' ? `${nodeName.toLowerCase()} - "error" >> ${errorNodeCode}` : ''}
`;

  return [nodeName.toLowerCase(), Blockly.Python.ORDER_ATOMIC];
};