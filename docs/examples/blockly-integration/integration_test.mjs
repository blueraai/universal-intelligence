/**
 * Headless integration tests for Universal Agents Blockly integration.
 * This file contains tests that can be run without a browser environment,
 * using Node.js and the Blockly headless module.
 * 
 * To run these tests:
 * 1. Install Node.js dependencies: npm install blockly jsdom
 * 2. Run: node integration_test.js
 */

// Import required modules
import * as Blockly from 'blockly';
import { JSDOM } from 'jsdom';

// Create a virtual DOM for Blockly to use
const dom = new JSDOM(`
<!DOCTYPE html>
<html>
<body>
  <div id="blocklyDiv" style="height: 480px; width: 600px;"></div>
</body>
</html>
`, { pretendToBeVisual: true });

// Set up global objects to mimic browser environment
global.window = dom.window;
global.document = dom.window.document;
global.XMLHttpRequest = dom.window.XMLHttpRequest;

// Test suite functions
function assertEquals(actual, expected, message) {
  if (actual !== expected) {
    throw new Error(message || `Expected ${expected}, but got ${actual}`);
  }
}

function assertTrue(condition, message) {
  if (!condition) {
    throw new Error(message || 'Assertion failed: expected true but got false');
  }
}

function assertFalse(condition, message) {
  if (condition) {
    throw new Error(message || 'Assertion failed: expected false but got true');
  }
}

function assertNotNull(value, message) {
  if (value === null || value === undefined) {
    throw new Error(message || 'Assertion failed: value is null or undefined');
  }
}

function assertContains(text, substring, message) {
  if (!text.includes(substring)) {
    throw new Error(message || `Expected text to contain "${substring}" but it doesn't`);
  }
}

// Load block definitions
function loadBlockDefinitions() {
  // Define the basic node block
  Blockly.Blocks['universal_agents_node'] = {
    init: function() {
      this.appendDummyInput()
          .appendField("Node")
          .appendField(new Blockly.FieldTextInput("MyNode"), "NODE_NAME");
      
      this.appendStatementInput("PREP")
          .setCheck(null)
          .appendField("prep");
      
      this.appendStatementInput("EXEC")
          .setCheck(null)
          .appendField("exec");
      
      this.appendStatementInput("POST")
          .setCheck(null)
          .appendField("post");
      
      this.setOutput(true, "NODE");
      
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
      this.setHelpUrl("");
    }
  };

  // Define the flow block
  Blockly.Blocks['universal_agents_flow'] = {
    init: function() {
      this.appendDummyInput()
          .appendField("Flow")
          .appendField(new Blockly.FieldTextInput("MyFlow"), "FLOW_NAME");
      
      this.appendValueInput("START_NODE")
          .setCheck("NODE")
          .appendField("start");
      
      this.appendDummyInput()
          .appendField("visualization")
          .appendField(new Blockly.FieldCheckbox("FALSE"), "VISUALIZATION");
      
      this.appendDummyInput()
          .appendField("path")
          .appendField(new Blockly.FieldTextInput("visualizations"), "VIZ_PATH");
      
      this.setOutput(true, "FLOW");
      
      this.setColour(160);
      this.setTooltip("Creates a Universal Agents Flow with the specified start node");
      this.setHelpUrl("");
    }
  };

  // Define the model node block
  Blockly.Blocks['universal_model_node'] = {
    init: function() {
      this.appendDummyInput()
          .appendField("ModelNode")
          .appendField(new Blockly.FieldTextInput("MyModelNode"), "NODE_NAME");
      
      this.appendDummyInput()
          .appendField("model")
          .appendField(new Blockly.FieldDropdown([
            ["Default", "UniversalModel()"],
            ["Llama3-8B", "Llama3Model()"],
            ["Qwen2-7B", "Qwen2Model()"],
            ["CustomModel", "CustomModel()"]
          ]), "MODEL");
      
      this.appendDummyInput()
          .appendField("prompt template:");
      this.appendDummyInput()
          .appendField(new Blockly.FieldTextInput("Please answer: {question}"), "PROMPT_TEMPLATE");
      
      this.appendDummyInput()
          .appendField("input keys:")
          .appendField(new Blockly.FieldTextInput("question"), "INPUT_KEYS");
      
      this.appendDummyInput()
          .appendField("output key:")
          .appendField(new Blockly.FieldTextInput("answer"), "OUTPUT_KEY");
      
      this.appendDummyInput()
          .appendField("parameters:");
      this.appendDummyInput()
          .appendField("temperature:")
          .appendField(new Blockly.FieldNumber(0.7), "TEMPERATURE");
      this.appendDummyInput()
          .appendField("max tokens:")
          .appendField(new Blockly.FieldNumber(1000), "MAX_TOKENS");
      
      this.setOutput(true, "NODE");
      
      this.appendValueInput("ACTION_NEXT")
          .setCheck("NODE")
          .appendField("next →");
      
      this.appendValueInput("ACTION_ERROR")
          .setCheck("NODE")
          .appendField("error →");
      
      this.setColour(290);
      this.setTooltip("Creates a Universal Model Node for using language models");
      this.setHelpUrl("");
    }
  };

  // Define JavaScript generators
  Blockly.JavaScript['universal_agents_node'] = function(block) {
    var nodeName = block.getFieldValue('NODE_NAME');
    var prepCode = Blockly.JavaScript.statementToCode(block, 'PREP');
    var execCode = Blockly.JavaScript.statementToCode(block, 'EXEC');
    var postCode = Blockly.JavaScript.statementToCode(block, 'POST');
    
    var code = `const ${nodeName.toLowerCase()} = new Node("${nodeName}");`;
    return [nodeName.toLowerCase(), Blockly.JavaScript.ORDER_ATOMIC];
  };

  Blockly.JavaScript['universal_agents_flow'] = function(block) {
    var flowName = block.getFieldValue('FLOW_NAME');
    var startNodeCode = Blockly.JavaScript.valueToCode(block, 'START_NODE', Blockly.JavaScript.ORDER_ATOMIC) || 'null';
    var visualization = block.getFieldValue('VISUALIZATION') === 'TRUE';
    
    var code = `const ${flowName.toLowerCase()} = new Flow(${startNodeCode}, "${flowName}");`;
    return [flowName.toLowerCase(), Blockly.JavaScript.ORDER_ATOMIC];
  };

  Blockly.JavaScript['universal_model_node'] = function(block) {
    var nodeName = block.getFieldValue('NODE_NAME');
    var model = block.getFieldValue('MODEL');
    
    var code = `const ${nodeName.toLowerCase()} = new ModelNode(${model});`;
    return [nodeName.toLowerCase(), Blockly.JavaScript.ORDER_ATOMIC];
  };

  // Python generators
  Blockly.Python = Blockly.Python || {};
  Blockly.Python['universal_agents_node'] = function(block) {
    var nodeName = block.getFieldValue('NODE_NAME');
    var prepCode = Blockly.JavaScript.statementToCode(block, 'PREP');
    var execCode = Blockly.JavaScript.statementToCode(block, 'EXEC');
    var postCode = Blockly.JavaScript.statementToCode(block, 'POST');
    
    var code = `${nodeName.toLowerCase()} = Node("${nodeName}")`;
    return [nodeName.toLowerCase(), Blockly.Python.ORDER_ATOMIC];
  };

  Blockly.Python['universal_agents_flow'] = function(block) {
    var flowName = block.getFieldValue('FLOW_NAME');
    var startNodeCode = Blockly.Python.valueToCode(block, 'START_NODE', Blockly.Python.ORDER_ATOMIC) || 'None';
    
    var code = `${flowName.toLowerCase()} = Flow(${startNodeCode}, "${flowName}")`;
    return [flowName.toLowerCase(), Blockly.Python.ORDER_ATOMIC];
  };

  Blockly.Python['universal_model_node'] = function(block) {
    var nodeName = block.getFieldValue('NODE_NAME');
    var model = block.getFieldValue('MODEL');
    
    var code = `${nodeName.toLowerCase()} = ModelNode(${model})`;
    return [nodeName.toLowerCase(), Blockly.Python.ORDER_ATOMIC];
  };
}

// Initialize Blockly workspace
function setupWorkspace() {
  // Create a headless workspace
  const workspace = new Blockly.Workspace();
  return workspace;
}

// Test: Create a basic node
function testBasicNodeCreation(workspace) {
  console.log('Test: Basic Node Creation');
  
  // Create a node block
  const nodeBlock = workspace.newBlock('universal_agents_node');
  nodeBlock.setFieldValue('TestNode', 'NODE_NAME');
  
  // Verify the block exists
  assertNotNull(nodeBlock, 'Node block should be created');
  assertEquals(nodeBlock.type, 'universal_agents_node', 'Block should be of type universal_agents_node');
  assertEquals(nodeBlock.getFieldValue('NODE_NAME'), 'TestNode', 'Node name should be set correctly');
  
  // Generate code
  const jsCode = Blockly.JavaScript.blockToCode(nodeBlock);
  assertNotNull(jsCode, 'Generated JavaScript code should not be null');
  assertContains(jsCode, 'testnode', 'Generated code should contain the node variable');
  
  // Generate Python code
  const pyCode = Blockly.Python.blockToCode(nodeBlock);
  assertNotNull(pyCode, 'Generated Python code should not be null');
  assertContains(pyCode, 'testnode', 'Generated Python code should contain the node variable');
  
  console.log('✓ Basic Node Creation: PASSED\n');
}

// Test: Create a flow
function testFlowCreation(workspace) {
  console.log('Test: Flow Creation');
  
  // Create a flow block
  const flowBlock = workspace.newBlock('universal_agents_flow');
  flowBlock.setFieldValue('TestFlow', 'FLOW_NAME');
  
  // Verify the block exists
  assertNotNull(flowBlock, 'Flow block should be created');
  assertEquals(flowBlock.type, 'universal_agents_flow', 'Block should be of type universal_agents_flow');
  assertEquals(flowBlock.getFieldValue('FLOW_NAME'), 'TestFlow', 'Flow name should be set correctly');
  
  // Generate code
  const jsCode = Blockly.JavaScript.blockToCode(flowBlock);
  assertNotNull(jsCode, 'Generated JavaScript code should not be null');
  assertContains(jsCode, 'testflow', 'Generated code should contain the flow variable');
  
  // Generate Python code
  const pyCode = Blockly.Python.blockToCode(flowBlock);
  assertNotNull(pyCode, 'Generated Python code should not be null');
  assertContains(pyCode, 'testflow', 'Generated Python code should contain the flow variable');
  
  console.log('✓ Flow Creation: PASSED\n');
}

// Test: Create a model node
function testModelNodeCreation(workspace) {
  console.log('Test: Model Node Creation');
  
  // Create a model node block
  const modelNodeBlock = workspace.newBlock('universal_model_node');
  modelNodeBlock.setFieldValue('TestModelNode', 'NODE_NAME');
  
  // Verify the block exists
  assertNotNull(modelNodeBlock, 'Model node block should be created');
  assertEquals(modelNodeBlock.type, 'universal_model_node', 'Block should be of type universal_model_node');
  assertEquals(modelNodeBlock.getFieldValue('NODE_NAME'), 'TestModelNode', 'Model node name should be set correctly');
  
  // Generate code
  const jsCode = Blockly.JavaScript.blockToCode(modelNodeBlock);
  assertNotNull(jsCode, 'Generated JavaScript code should not be null');
  assertContains(jsCode, 'testmodelnode', 'Generated code should contain the model node variable');
  
  // Generate Python code
  const pyCode = Blockly.Python.blockToCode(modelNodeBlock);
  assertNotNull(pyCode, 'Generated Python code should not be null');
  assertContains(pyCode, 'testmodelnode', 'Generated Python code should contain the model node variable');
  
  console.log('✓ Model Node Creation: PASSED\n');
}

// Test: Connect nodes in a flow
function testNodeConnections(workspace) {
  console.log('Test: Node Connections');
  
  // Create blocks
  const nodeBlock1 = workspace.newBlock('universal_agents_node');
  nodeBlock1.setFieldValue('FirstNode', 'NODE_NAME');
  
  const nodeBlock2 = workspace.newBlock('universal_agents_node');
  nodeBlock2.setFieldValue('SecondNode', 'NODE_NAME');
  
  const flowBlock = workspace.newBlock('universal_agents_flow');
  flowBlock.setFieldValue('TestFlow', 'FLOW_NAME');
  
  // Connect blocks
  const startNodeInput = flowBlock.getInput('START_NODE');
  startNodeInput.connection.connect(nodeBlock1.outputConnection);
  
  const nextNodeInput = nodeBlock1.getInput('ACTION_NEXT');
  nextNodeInput.connection.connect(nodeBlock2.outputConnection);
  
  // Verify connections
  assertTrue(nodeBlock1.outputConnection.isConnected(), 'First node should be connected to flow');
  assertTrue(nextNodeInput.connection.isConnected(), 'Second node should be connected to first node');
  
  // Generate code
  const jsCode = Blockly.JavaScript.blockToCode(flowBlock);
  assertNotNull(jsCode, 'Generated JavaScript code should not be null');
  
  // Check that flow references first node
  assertContains(jsCode, 'firstnode', 'Generated code should contain the first node variable');
  
  console.log('✓ Node Connections: PASSED\n');
}

// Test: Full workflow
function testCompleteWorkflow(workspace) {
  console.log('Test: Complete Workflow');
  
  // Create model node
  const modelNode = workspace.newBlock('universal_model_node');
  modelNode.setFieldValue('Processor', 'NODE_NAME');
  modelNode.setFieldValue('UniversalModel()', 'MODEL');
  modelNode.setFieldValue('question', 'INPUT_KEYS');
  modelNode.setFieldValue('answer', 'OUTPUT_KEY');
  
  // Create output node
  const outputNode = workspace.newBlock('universal_agents_node');
  outputNode.setFieldValue('Output', 'NODE_NAME');
  
  // Create flow
  const flowBlock = workspace.newBlock('universal_agents_flow');
  flowBlock.setFieldValue('WorkflowFlow', 'FLOW_NAME');
  flowBlock.setFieldValue('TRUE', 'VISUALIZATION');
  
  // Connect nodes
  const startNodeInput = flowBlock.getInput('START_NODE');
  startNodeInput.connection.connect(modelNode.outputConnection);
  
  const nextNodeInput = modelNode.getInput('ACTION_NEXT');
  nextNodeInput.connection.connect(outputNode.outputConnection);
  
  // Verify connections
  assertTrue(modelNode.outputConnection.isConnected(), 'Model node should be connected to flow');
  assertTrue(nextNodeInput.connection.isConnected(), 'Output node should be connected to model node');
  
  // Generate code
  const jsCode = Blockly.JavaScript.workspaceToCode(workspace);
  assertNotNull(jsCode, 'Generated JavaScript code should not be null');
  
  // Check for expected elements in the code
  assertContains(jsCode, 'processor', 'Generated code should contain the processor node');
  assertContains(jsCode, 'output', 'Generated code should contain the output node');
  assertContains(jsCode, 'workflowflow', 'Generated code should contain the flow');
  
  console.log('✓ Complete Workflow: PASSED\n');
}

// Run all tests
async function runTests() {
  console.log('Running Universal Agents Blockly Integration Tests\n');
  
  try {
    // Load block definitions
    loadBlockDefinitions();
    
    // Set up workspace
    const workspace = setupWorkspace();
    
    // Run tests
    testBasicNodeCreation(workspace);
    testFlowCreation(workspace);
    testModelNodeCreation(workspace);
    testNodeConnections(workspace);
    testCompleteWorkflow(workspace);
    
    console.log('\nAll tests PASSED! 🎉');
    return true;
  } catch (error) {
    console.error(`\n❌ TEST FAILED: ${error.message}`);
    console.error(error.stack);
    return false;
  }
}

// Run tests
runTests().then(success => {
  process.exit(success ? 0 : 1);
});