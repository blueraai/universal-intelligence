/**
 * Toolbox configuration for Universal Agents Blockly integration.
 * This defines the categories and blocks available in the Blockly editor.
 */

// Define the toolbox configuration in XML format
var toolboxConfig = {
  "kind": "categoryToolbox",
  "contents": [
    {
      "kind": "category",
      "name": "Core",
      "colour": "#5C81A6",
      "contents": [
        {
          "kind": "block",
          "type": "universal_agents_node"
        },
        {
          "kind": "block",
          "type": "universal_agents_flow"
        }
      ]
    },
    {
      "kind": "category",
      "name": "Universal Integration",
      "colour": "#A65C94",
      "contents": [
        {
          "kind": "block",
          "type": "universal_model_node"
        },
        {
          "kind": "block",
          "type": "universal_tool_node"
        },
        {
          "kind": "block",
          "type": "universal_agent_node"
        }
      ]
    },
    {
      "kind": "category",
      "name": "Patterns",
      "colour": "#5CA694",
      "contents": [
        {
          "kind": "block",
          "type": "rag_pattern"
        },
        {
          "kind": "block",
          "type": "map_reduce_pattern"
        },
        {
          "kind": "block",
          "type": "multi_agent_pattern"
        },
        {
          "kind": "block",
          "type": "workflow_pattern"
        }
      ]
    },
    {
      "kind": "category",
      "name": "Inputs/Outputs",
      "colour": "#A6745C",
      "contents": [
        {
          "kind": "block",
          "type": "input_node"
        },
        {
          "kind": "block",
          "type": "output_node"
        },
        {
          "kind": "block",
          "type": "processing_node"
        }
      ]
    },
    {
      "kind": "category",
      "name": "Logic",
      "colour": "#5C67A6",
      "contents": [
        {
          "kind": "block",
          "type": "conditional_node"
        },
        {
          "kind": "block",
          "type": "switch_node"
        },
        {
          "kind": "block",
          "type": "loop_node"
        }
      ]
    },
    {
      "kind": "category",
      "name": "Advanced",
      "colour": "#A65C6E",
      "contents": [
        {
          "kind": "block",
          "type": "batch_node"
        },
        {
          "kind": "block",
          "type": "async_node"
        },
        {
          "kind": "block",
          "type": "error_handler_node"
        }
      ]
    },
    {
      "kind": "category",
      "name": "Templates",
      "colour": "#5CA65C",
      "contents": [
        {
          "kind": "block",
          "type": "chat_template"
        },
        {
          "kind": "block",
          "type": "search_template"
        },
        {
          "kind": "block",
          "type": "analysis_template"
        }
      ]
    },
    {
      "kind": "category",
      "name": "State",
      "colour": "#A69B5C",
      "contents": [
        {
          "kind": "block",
          "type": "get_shared_value"
        },
        {
          "kind": "block",
          "type": "set_shared_value"
        },
        {
          "kind": "block",
          "type": "state_transformation"
        }
      ]
    }
  ]
};

// Initialize Blockly with the toolbox
Blockly.inject('blocklyDiv', {
  toolbox: toolboxConfig,
  grid: {
    spacing: 20,
    length: 3,
    colour: '#ccc',
    snap: true
  },
  zoom: {
    controls: true,
    wheel: true,
    startScale: 1.0,
    maxScale: 3,
    minScale: 0.3,
    scaleSpeed: 1.2
  },
  trashcan: true,
  theme: Blockly.Themes.Classic
});

// Add event listener for block changes to update code
var workspace = Blockly.getMainWorkspace();
workspace.addChangeListener(updateCode);

// Function to update the generated code
function updateCode(event) {
  var code = Blockly.JavaScript.workspaceToCode(workspace);
  document.getElementById('codeDiv').innerHTML = code;
  
  var pythonCode = Blockly.Python.workspaceToCode(workspace);
  document.getElementById('pythonCodeDiv').innerHTML = pythonCode;
}

// Add event listener for the run button
document.getElementById('runButton').addEventListener('click', function() {
  // In a full implementation, this would execute the generated code
  console.log('Running code...');
  highlightCurrentExecution();
});

// Add event listener for the save button
document.getElementById('saveButton').addEventListener('click', function() {
  var xmlDom = Blockly.Xml.workspaceToDom(workspace);
  var xmlText = Blockly.Xml.domToPrettyText(xmlDom);
  
  // Save the XML to localStorage
  localStorage.setItem('universalAgentsBlocks', xmlText);
  console.log('Blocks saved to localStorage');
});

// Add event listener for the load button
document.getElementById('loadButton').addEventListener('click', function() {
  var xmlText = localStorage.getItem('universalAgentsBlocks');
  if (xmlText) {
    workspace.clear();
    var xmlDom = Blockly.Xml.textToDom(xmlText);
    Blockly.Xml.domToWorkspace(xmlDom, workspace);
    console.log('Blocks loaded from localStorage');
  } else {
    console.log('No saved blocks found');
  }
});

// Function to simulate execution highlighting
function highlightCurrentExecution() {
  var blocks = workspace.getAllBlocks(false);
  var i = 0;
  
  function highlightNextBlock() {
    if (i < blocks.length) {
      // Clear previous highlighting
      if (i > 0) {
        blocks[i-1].setHighlighted(false);
      }
      
      // Highlight current block
      blocks[i].setHighlighted(true);
      i++;
      
      // Schedule next highlight
      setTimeout(highlightNextBlock, 500);
    } else {
      // Clear final block highlighting
      blocks[blocks.length-1].setHighlighted(false);
    }
  }
  
  highlightNextBlock();
}