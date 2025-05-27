// Custom block definitions for Universal Intelligence components

// Simple console logger for custom blocks (since we can't use ES modules here)
const blockLog = {
    debug: (...args) => console.log('\x1b[36m[DEBUG]\x1b[0m custom-blocks.js:', ...args),
    info: (...args) => console.log('\x1b[32m[INFO]\x1b[0m custom-blocks.js:', ...args),
    warn: (...args) => console.log('\x1b[33m[WARN]\x1b[0m custom-blocks.js:', ...args),
    error: (...args) => console.log('\x1b[31m[ERROR]\x1b[0m custom-blocks.js:', ...args)
};

blockLog.info('initializing custom blocks');

// Block definitions can be done immediately
// Model Blocks
blockLog.debug('defining block', 'uin_model_local');
Blockly.Blocks['uin_model_local'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Create Local Model 🧠");
    this.appendDummyInput()
        .appendField("engine")
        .appendField(new Blockly.FieldDropdown([
            ["auto", "AUTO"],
            ["transformers", "TRANSFORMERS"],
            ["llama.cpp", "LLAMA_CPP"],
            ["mlx", "MLX"]
        ]), "ENGINE");
    this.appendDummyInput()
        .appendField("quantization")
        .appendField(new Blockly.FieldDropdown([
            ["auto", "AUTO"],
            ["4-bit", "4BIT"],
            ["8-bit", "8BIT"],
            ["16-bit", "16BIT"]
        ]), "QUANTIZATION");
    this.setOutput(true, "Model");
    this.setColour(195);
    this.setTooltip("Create a local Universal Model");
  }
};

blockLog.debug('defining block', 'uin_model_remote');
Blockly.Blocks['uin_model_remote'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Create Remote Model ☁️");
    this.appendValueInput("CREDENTIALS")
        .setCheck("String")
        .appendField("API key");
    this.appendDummyInput()
        .appendField("provider")
        .appendField(new Blockly.FieldDropdown([
            ["OpenRouter", "OPENROUTER"],
            ["OpenAI", "OPENAI"],
            ["Anthropic", "ANTHROPIC"],
            ["Google", "GOOGLE"]
        ]), "PROVIDER");
    this.setOutput(true, "Model");
    this.setColour(195);
    this.setTooltip("Create a remote/cloud Universal Model");
  }
};

Blockly.Blocks['uin_model_process'] = {
  init: function() {
    this.appendValueInput("MODEL")
        .setCheck("Model")
        .appendField("Model process");
    this.appendValueInput("INPUT")
        .setCheck("String")
        .appendField("input");
    this.appendDummyInput()
        .appendField("remember")
        .appendField(new Blockly.FieldCheckbox("FALSE"), "REMEMBER");
    this.setOutput(true, "Result");
    this.setColour(195);
    this.setTooltip("Process input through a model");
  }
};

// Tool Blocks
blockLog.debug('defining block', 'uin_tool_printer');
Blockly.Blocks['uin_tool_printer'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Create Printer Tool 🖨️");
    this.setOutput(true, "Tool");
    this.setColour(120);
    this.setTooltip("Create a simple printer tool");
  }
};

Blockly.Blocks['uin_tool_api'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Create API Tool 🌐");
    this.setOutput(true, "Tool");
    this.setColour(120);
    this.setTooltip("Create an API caller tool");
  }
};

Blockly.Blocks['uin_tool_mcp'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Create MCP Tool 🔌");
    this.appendValueInput("SERVER")
        .setCheck("String")
        .appendField("MCP server");
    this.setOutput(true, "Tool");
    this.setColour(120);
    this.setTooltip("Create an MCP client tool");
  }
};

Blockly.Blocks['uin_tool_call'] = {
  init: function() {
    this.appendValueInput("TOOL")
        .setCheck("Tool")
        .appendField("Call tool");
    this.appendValueInput("METHOD")
        .setCheck("String")
        .appendField("method");
    this.appendValueInput("PARAMS")
        .appendField("parameters");
    this.setOutput(true, "Result");
    this.setColour(120);
    this.setTooltip("Call a tool method");
  }
};

// Agent Blocks
blockLog.debug('defining block', 'uin_agent_create');
Blockly.Blocks['uin_agent_create'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Create Agent 🤖");
    this.appendValueInput("MODEL")
        .setCheck("Model")
        .appendField("model");
    this.appendValueInput("TOOLS")
        .setCheck("Array")
        .appendField("tools");
    this.appendValueInput("TEAM")
        .setCheck("Array")
        .appendField("team");
    this.setOutput(true, "Agent");
    this.setColour(30);
    this.setTooltip("Create a Universal Agent");
  }
};

Blockly.Blocks['uin_agent_process'] = {
  init: function() {
    this.appendValueInput("AGENT")
        .setCheck("Agent")
        .appendField("Agent process");
    this.appendValueInput("INPUT")
        .setCheck("String")
        .appendField("task");
    this.appendValueInput("EXTRA_TOOLS")
        .setCheck("Array")
        .appendField("extra tools");
    this.appendDummyInput()
        .appendField("remember")
        .appendField(new Blockly.FieldCheckbox("FALSE"), "REMEMBER");
    this.setOutput(true, "Result");
    this.setColour(30);
    this.setTooltip("Process a task through an agent");
  }
};

Blockly.Blocks['uin_agent_connect'] = {
  init: function() {
    this.appendValueInput("AGENT")
        .setCheck("Agent")
        .appendField("Connect to agent");
    this.appendValueInput("TOOLS")
        .setCheck("Array")
        .appendField("add tools");
    this.appendValueInput("AGENTS")
        .setCheck("Array")
        .appendField("add agents");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(30);
    this.setTooltip("Connect tools and agents to an existing agent");
  }
};

// Wait for DOM and generators to be ready before defining code generators
if (document.readyState === 'loading') {
    blockLog.debug('DOM loading, adding DOMContentLoaded listener');
    document.addEventListener('DOMContentLoaded', initializeGenerators);
} else {
    // DOM is already loaded
    blockLog.debug('DOM already loaded, scheduling generator initialization');
    setTimeout(initializeGenerators, 100);
}

function initializeGenerators() {
    blockLog.debug('initializeGenerators()', 'checking if generators are available');
    
    // Check if generators are available
    if (typeof Blockly.Python === 'undefined' || typeof Blockly.JavaScript === 'undefined') {
        blockLog.debug('initializeGenerators()', 'generators not available yet, retrying in 100ms');
        setTimeout(initializeGenerators, 100);
        return;
    }

    blockLog.info('initializeGenerators()', 'Blockly generators available, initializing UIN code generators');
    
    // Set a global flag to indicate generators are being initialized
    window.uinGeneratorsInitializing = true;
    blockLog.debug('initializeGenerators()', 'set window.uinGeneratorsInitializing = true');

    // Code Generators for Python
    Blockly.Python['uin_model_local'] = function(block) {
      var engine = block.getFieldValue('ENGINE');
      var quantization = block.getFieldValue('QUANTIZATION');
      
      var engineValue = engine === 'AUTO' ? 'None' : `"${engine.toLowerCase()}"`;
      var quantValue = quantization === 'AUTO' ? 'None' : `"${quantization}"`;
      
      var code = `Model(engine=${engineValue}, quantization=${quantValue})`;
      return [code, Blockly.Python.ORDER_ATOMIC];
    };

    Blockly.Python['uin_model_remote'] = function(block) {
      var credentials = Blockly.Python.valueToCode(block, 'CREDENTIALS', Blockly.Python.ORDER_ATOMIC) || '""';
      var provider = block.getFieldValue('PROVIDER');
      
      var code = `RemoteModel(credentials=${credentials})`;
      return [code, Blockly.Python.ORDER_ATOMIC];
    };

    Blockly.Python['uin_model_process'] = function(block) {
      var model = Blockly.Python.valueToCode(block, 'MODEL', Blockly.Python.ORDER_ATOMIC) || 'None';
      var input = Blockly.Python.valueToCode(block, 'INPUT', Blockly.Python.ORDER_ATOMIC) || '""';
      var remember = block.getFieldValue('REMEMBER') === 'TRUE';
      
      var code = `${model}.process(${input}, remember=${remember ? 'True' : 'False'})`;
      return [code, Blockly.Python.ORDER_ATOMIC];
    };

    Blockly.Python['uin_tool_printer'] = function(block) {
      var code = 'Tool()  # Configure with print_text method';
      return [code, Blockly.Python.ORDER_ATOMIC];
    };

    Blockly.Python['uin_tool_api'] = function(block) {
      var code = 'Tool()  # Configure with API methods';
      return [code, Blockly.Python.ORDER_ATOMIC];
    };

    Blockly.Python['uin_tool_mcp'] = function(block) {
      var server = Blockly.Python.valueToCode(block, 'SERVER', Blockly.Python.ORDER_ATOMIC) || '""';
      var code = `MCPTool(server=${server})`;
      return [code, Blockly.Python.ORDER_ATOMIC];
    };

    Blockly.Python['uin_tool_call'] = function(block) {
      var tool = Blockly.Python.valueToCode(block, 'TOOL', Blockly.Python.ORDER_ATOMIC) || 'None';
      var method = Blockly.Python.valueToCode(block, 'METHOD', Blockly.Python.ORDER_ATOMIC) || '""';
      var params = Blockly.Python.valueToCode(block, 'PARAMS', Blockly.Python.ORDER_ATOMIC) || '{}';
      
      // Remove quotes from method name
      method = method.replace(/['"]/g, '');
      
      var code = `${tool}.${method}(**${params})`;
      return [code, Blockly.Python.ORDER_ATOMIC];
    };

    Blockly.Python['uin_agent_create'] = function(block) {
      var model = Blockly.Python.valueToCode(block, 'MODEL', Blockly.Python.ORDER_ATOMIC);
      var tools = Blockly.Python.valueToCode(block, 'TOOLS', Blockly.Python.ORDER_ATOMIC);
      var team = Blockly.Python.valueToCode(block, 'TEAM', Blockly.Python.ORDER_ATOMIC);
      
      var args = [];
      if (model) args.push(`model=${model}`);
      if (tools) args.push(`expand_tools=${tools}`);
      if (team) args.push(`expand_team=${team}`);
      
      var code = `Agent(${args.join(', ')})`;
      return [code, Blockly.Python.ORDER_ATOMIC];
    };

    Blockly.Python['uin_agent_process'] = function(block) {
      var agent = Blockly.Python.valueToCode(block, 'AGENT', Blockly.Python.ORDER_ATOMIC) || 'None';
      var input = Blockly.Python.valueToCode(block, 'INPUT', Blockly.Python.ORDER_ATOMIC) || '""';
      var extraTools = Blockly.Python.valueToCode(block, 'EXTRA_TOOLS', Blockly.Python.ORDER_ATOMIC);
      var remember = block.getFieldValue('REMEMBER') === 'TRUE';
      
      var args = [input];
      if (extraTools) args.push(`extra_tools=${extraTools}`);
      args.push(`remember=${remember ? 'True' : 'False'}`);
      
      var code = `${agent}.process(${args.join(', ')})`;
      return [code, Blockly.Python.ORDER_ATOMIC];
    };

    Blockly.Python['uin_agent_connect'] = function(block) {
      var agent = Blockly.Python.valueToCode(block, 'AGENT', Blockly.Python.ORDER_ATOMIC) || 'None';
      var tools = Blockly.Python.valueToCode(block, 'TOOLS', Blockly.Python.ORDER_ATOMIC);
      var agents = Blockly.Python.valueToCode(block, 'AGENTS', Blockly.Python.ORDER_ATOMIC);
      
      var args = [];
      if (tools) args.push(`tools=${tools}`);
      if (agents) args.push(`agents=${agents}`);
      
      var code = `${agent}.connect(${args.join(', ')})\n`;
      return code;
    };

    // JavaScript Code Generators
    Blockly.JavaScript['uin_model_local'] = function(block) {
      var engine = block.getFieldValue('ENGINE');
      var quantization = block.getFieldValue('QUANTIZATION');
      
      var options = {};
      if (engine !== 'AUTO') options.engine = engine.toLowerCase();
      if (quantization !== 'AUTO') options.quantization = quantization;
      
      var code = `new Model(${JSON.stringify(options)})`;
      return [code, Blockly.JavaScript.ORDER_ATOMIC];
    };

    Blockly.JavaScript['uin_model_remote'] = function(block) {
      var credentials = Blockly.JavaScript.valueToCode(block, 'CREDENTIALS', Blockly.JavaScript.ORDER_ATOMIC) || '""';
      
      var code = `new RemoteModel({ credentials: ${credentials} })`;
      return [code, Blockly.JavaScript.ORDER_ATOMIC];
    };

    Blockly.JavaScript['uin_model_process'] = function(block) {
      var model = Blockly.JavaScript.valueToCode(block, 'MODEL', Blockly.JavaScript.ORDER_ATOMIC) || 'null';
      var input = Blockly.JavaScript.valueToCode(block, 'INPUT', Blockly.JavaScript.ORDER_ATOMIC) || '""';
      var remember = block.getFieldValue('REMEMBER') === 'TRUE';
      
      var code = `await ${model}.process(${input}, { remember: ${remember} })`;
      return [code, Blockly.JavaScript.ORDER_ATOMIC];
    };

    Blockly.JavaScript['uin_tool_printer'] = function(block) {
      // Create a Tool with a printText method
      var code = `(() => {
        const tool = new Tool();
        tool.printText = function(params) {
          const text = params?.text || params;
          console.log(text);
          return [text, { printed: true }];
        };
        return tool;
      })()`;
      return [code, Blockly.JavaScript.ORDER_ATOMIC];
    };

    Blockly.JavaScript['uin_tool_api'] = function(block) {
      // Create a Tool with API calling capabilities
      var code = `(() => {
        const tool = new Tool();
        tool.fetch = async function(params) {
          try {
            const response = await fetch(params.url, params.options || {});
            const data = await response.json();
            return [data, { status: response.status }];
          } catch (error) {
            return [null, { error: error.message }];
          }
        };
        return tool;
      })()`;
      return [code, Blockly.JavaScript.ORDER_ATOMIC];
    };

    Blockly.JavaScript['uin_tool_mcp'] = function(block) {
      var server = Blockly.JavaScript.valueToCode(block, 'SERVER', Blockly.JavaScript.ORDER_ATOMIC) || '""';
      var code = `new MCPTool({ server: ${server} })`;
      return [code, Blockly.JavaScript.ORDER_ATOMIC];
    };

    Blockly.JavaScript['uin_tool_call'] = function(block) {
      var tool = Blockly.JavaScript.valueToCode(block, 'TOOL', Blockly.JavaScript.ORDER_ATOMIC) || 'null';
      var method = Blockly.JavaScript.valueToCode(block, 'METHOD', Blockly.JavaScript.ORDER_ATOMIC) || '""';
      var params = Blockly.JavaScript.valueToCode(block, 'PARAMS', Blockly.JavaScript.ORDER_ATOMIC) || '{}';
      
      // Remove quotes from method name
      method = method.replace(/['"]/g, '');
      
      var code = `await ${tool}.${method}(${params})`;
      return [code, Blockly.JavaScript.ORDER_ATOMIC];
    };

    Blockly.JavaScript['uin_agent_create'] = function(block) {
      var model = Blockly.JavaScript.valueToCode(block, 'MODEL', Blockly.JavaScript.ORDER_ATOMIC);
      var tools = Blockly.JavaScript.valueToCode(block, 'TOOLS', Blockly.JavaScript.ORDER_ATOMIC);
      var team = Blockly.JavaScript.valueToCode(block, 'TEAM', Blockly.JavaScript.ORDER_ATOMIC);
      
      var args = [];
      if (model || tools || team) {
        var obj = {};
        if (model) obj.model = '__MODEL__';
        if (tools) obj.expandTools = '__TOOLS__';
        if (team) obj.expandTeam = '__TEAM__';
        
        var objStr = JSON.stringify(obj);
        if (model) objStr = objStr.replace('"__MODEL__"', model);
        if (tools) objStr = objStr.replace('"__TOOLS__"', tools);
        if (team) objStr = objStr.replace('"__TEAM__"', team);
        
        args.push(objStr);
      }
      
      var code = `new Agent(${args.join('')})`;
      return [code, Blockly.JavaScript.ORDER_ATOMIC];
    };

    Blockly.JavaScript['uin_agent_process'] = function(block) {
      var agent = Blockly.JavaScript.valueToCode(block, 'AGENT', Blockly.JavaScript.ORDER_ATOMIC) || 'null';
      var input = Blockly.JavaScript.valueToCode(block, 'INPUT', Blockly.JavaScript.ORDER_ATOMIC) || '""';
      var extraTools = Blockly.JavaScript.valueToCode(block, 'EXTRA_TOOLS', Blockly.JavaScript.ORDER_ATOMIC);
      var remember = block.getFieldValue('REMEMBER') === 'TRUE';
      
      var args = [input];
      if (extraTools || remember) {
        var obj = {};
        if (remember) obj.remember = remember;
        if (extraTools) obj.extraTools = '__EXTRA_TOOLS__';
        
        var objStr = JSON.stringify(obj);
        if (extraTools) objStr = objStr.replace('"__EXTRA_TOOLS__"', extraTools);
        
        args.push(objStr);
      }
      
      var code = `await ${agent}.process(${args.join(', ')})`;
      return [code, Blockly.JavaScript.ORDER_ATOMIC];
    };

    Blockly.JavaScript['uin_agent_connect'] = function(block) {
      var agent = Blockly.JavaScript.valueToCode(block, 'AGENT', Blockly.JavaScript.ORDER_ATOMIC) || 'null';
      var tools = Blockly.JavaScript.valueToCode(block, 'TOOLS', Blockly.JavaScript.ORDER_ATOMIC);
      var agents = Blockly.JavaScript.valueToCode(block, 'AGENTS', Blockly.JavaScript.ORDER_ATOMIC);
      
      var args = [];
      if (tools || agents) {
        var obj = {};
        if (tools) obj.tools = '__TOOLS__';
        if (agents) obj.agents = '__AGENTS__';
        
        var objStr = JSON.stringify(obj);
        if (tools) objStr = objStr.replace('"__TOOLS__"', tools);
        if (agents) objStr = objStr.replace('"__AGENTS__"', agents);
        
        args.push(objStr);
      }
      
      var code = `await ${agent}.connect(${args.join('')});\n`;
      return code;
    };
    
    // Set a global flag to indicate generators are ready
    window.uinGeneratorsReady = true;
    blockLog.info('initializeGenerators()', 'code generators initialized successfully');
    blockLog.debug('initializeGenerators()', 'set window.uinGeneratorsReady = true');
}