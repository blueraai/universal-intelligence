# Universal Intelligence Blockly Playground - Technical Documentation

A visual programming interface for [Universal Intelligence](https://github.com/blueraai/universal-intelligence) using Google Blockly. This proof-of-concept enables drag-and-drop composition of AI applications using Models, Tools, and Agents.

## Architecture Overview

### System Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Blockly UI    │────▶│  Code Generator  │────▶│ Browser Runtime │
│  (index.html)   │     │ (custom-blocks.js)│     │  (app-web.js)   │
└─────────────────┘     └──────────────────┘     └─────────────────┘
         │                                                 │
         └─────────────────┬───────────────────────────────┘
                           ▼
                    ┌─────────────┐
                    │  UIN Core   │
                    │  (ES Modules)│
                    └─────────────┘
```

### Key Components

#### 1. Custom Blocks (`custom-blocks.js`)

**Block Definitions**:
- Model blocks: `uin_model_local`, `uin_model_remote`, `uin_model_process`
- Tool blocks: `uin_tool_printer`, `uin_tool_api`, `uin_tool_fetch`, `uin_tool_mcp`, `uin_tool_call`
- Agent blocks: `uin_agent_create`, `uin_agent_research`, `uin_agent_process`, `uin_agent_connect`
- Utility blocks: `text_pretty_print`, `object_get_property`

**Code Generation**:
```javascript
// Example: Local Model Generator
Blockly.JavaScript.forBlock['uin_model_local'] = function(block) {
  var code = `await (async () => {
    console.log('🤖 Initializing local model...');
    try {
      const model = new Model();
      console.log('✅ Model ready:', model);
      return model;
    } catch (error) {
      console.error('❌ Model initialization failed:', error);
      throw error;
    }
  })()`;
  return [code, Blockly.JavaScript.ORDER_ATOMIC];
};
```

#### 2. Logger System (`logger.js`)

Centralized Pino-based logging with browser compatibility:

```javascript
const logger = pino({
  level: 'trace',
  browser: {
    serialize: false,
    asObject: false
  },
  hooks: {
    logMethod(inputArgs, method) {
      // CSS-styled console output
      console[config.console](
        `%c[${config.label}]%c`,
        `${config.color}; font-weight: bold`,
        'color: inherit',
        ...args
      );
    }
  }
});
```

#### 3. Main Application (`app-web.js`)

**Initialization**:
```javascript
// Global UIN component exposure
window.Model = Model;
window.RemoteModel = RemoteModel;
window.Agent = Agent;
window.Tool = Tool;
```

**Code Execution**:
```javascript
const asyncCode = `
  (async function() {
    const Model = window.Model;
    const Agent = window.Agent;
    const Tool = window.Tool;
    
    try {
      ${generatedCode}
    } catch (error) {
      console.error('Execution error:', error);
    }
  })()
`;
await eval(asyncCode);
```

## Technical Implementation Details

### Universal Intelligence Integration

The playground imports UIN as ES modules:

```javascript
import universalintelligence, { Model, Agent, Tool, RemoteModel } from 'universalintelligence';
```

### Tuple Return Handling

All UIN methods return `[result, logs]` tuples. Generated code extracts results:

```javascript
// Model processing
result = (await model.process(input, { remember: false }))[0];

// Agent processing  
result = (await agent.process(task, { remember: true }))[0];

// Tool calls
result = (await tool.method(params))[0];
```

### Tool Implementation Pattern

Tools are created with method definitions:

```javascript
const fetchTool = new Tool();
fetchTool.fetchData = async function(params) {
  const url = params.url;
  try {
    const response = await fetch(url);
    const data = await response.json();
    return [data, { status: response.status, url: url }];
  } catch (error) {
    return [null, { error: error.message, url: url }];
  }
};
```

### Agent Creation with Tools

```javascript
const agent = new Agent({
  model: model,
  expandTools: [fetchTool, printerTool]
});
```

### Research Agent Implementation

The research agent is a specialized pattern:

```javascript
const researchAgent = new Agent({
  model: model,
  expandTools: [fetchTool, summaryTool]
});

researchAgent._sources = sources;
researchAgent.research = async function(query) {
  const prompt = 'You have fetchUrl and summarizeContent tools...';
  return await this.process(prompt);
};
```

## Block-to-Code Examples

### Model Creation
**Blocks**:
```
[Create Local Model] → [engine: AUTO] [quantization: AUTO]
```

**Generated JavaScript**:
```javascript
model = await (async () => {
  console.log('🤖 Initializing local model...');
  try {
    const model = new Model();
    console.log('✅ Model ready:', model);
    return model;
  } catch (error) {
    console.error('❌ Model initialization failed:', error);
    throw error;
  }
})();
```

### Agent with Tools
**Blocks**:
```
[Create Agent] → [model: modelVar] [tools: [fetchTool, printerTool]]
```

**Generated JavaScript**:
```javascript
multiAgent = new Agent({
  model: model,
  expandTools: [fetchTool, printerTool]
});
```

## Output Handling

### Pretty Print Modal
- 90% viewport width/height
- Scrollable content area
- CSS-styled modal with animations
- JSON formatting for objects

### Console Redirection
```javascript
const outputConsole = {
  logs: [],
  log: (...args) => { 
    this.logs.push(args.join(' ')); 
    updateOutput(); 
  },
  // Similar for warn, error, etc.
};

// Temporarily replace console during execution
window.console = outputConsole;
```

## Development Setup

### Dependencies
```json
{
  "dependencies": {
    "pino": "^8.16.0"
  },
  "devDependencies": {
    "pino-pretty": "^13.0.0",
    "vite": "^5.0.0"
  }
}
```

### Build Process
```bash
# Install dependencies
npm install

# Development server with HMR
npm run dev

# Production build
npm run build

# Preview production build
npm run preview
```

### Vite Configuration
```javascript
export default {
  root: '.',
  base: '/playground-blockly/',
  server: {
    port: 8001,
    open: '/playground-blockly/'
  }
};
```

## Advanced Features

### Dynamic Tool Connection
```javascript
await agent.connect({
  tools: [newTool1, newTool2],
  agents: [subAgent1, subAgent2]
});
```

### Memory Management
```javascript
// Remember parameter maintains conversation context
result = (await agent.process(input, { remember: true }))[0];
```

### Error Handling Patterns
```javascript
try {
  const model = new Model();
  // Success path
} catch (error) {
  console.error('Model initialization failed:', error);
  // Fallback behavior
}
```

## Known Technical Constraints

1. **Browser CORS**: External API calls subject to CORS restrictions
2. **WebGPU Requirements**: Local models require WebGPU-enabled browsers
3. **Memory Limits**: Browser memory constraints for large models
4. **Synchronous Limitations**: All operations wrapped in async for consistency

## Performance Considerations

- Model initialization is async and may take several seconds
- Use workspace clearing before loading new examples
- Minimize console output for better performance
- Consider model quantization options for memory efficiency

## Security Notes

- API keys are stored in browser memory only
- No server-side code execution
- All processing happens client-side
- CORS provides natural API access boundaries

## Extension Points

1. **Custom Blocks**: Add new blocks in `custom-blocks.js`
2. **Code Generators**: Implement new language targets
3. **Tool Implementations**: Create specialized tool patterns
4. **Agent Templates**: Pre-configured agent patterns

## Debugging

Enable verbose logging:
```javascript
log.level = 'trace';
```

Monitor execution flow:
- Model initialization logs
- Tool method calls
- Agent processing steps
- Error stack traces

## Contributing

When adding new features:
1. Define block in `custom-blocks.js`
2. Implement code generator
3. Add to toolbox in `index.html`
4. Create example if applicable
5. Update logger if needed

## License

Part of the Universal Intelligence project. See main repository for license details.