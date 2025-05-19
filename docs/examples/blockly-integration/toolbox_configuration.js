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

// The toolbox configuration is available as 'toolboxConfig' globally
// Workspace initialization will be handled by index.html