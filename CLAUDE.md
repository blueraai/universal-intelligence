# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Python Development
```bash
# Install base dependencies
pip install "universal-intelligence"

# Install with community components (choose based on your hardware)
pip install "universal-intelligence[community,mps]"     # Apple Silicon
pip install "universal-intelligence[community,cuda]"   # NVIDIA GPU
pip install "universal-intelligence[community]"        # CPU only

# Install development dependencies
pip install "universal-intelligence[dev]"

# Run example playground
python -m playground.example

# Linting (with ruff)
ruff check .
ruff check . --fix  # Auto-fix issues

# Formatting (with black and isort)
black .
isort .
```

### TypeScript/JavaScript Development
```bash
# Install dependencies
npm install

# Build TypeScript
npm run build

# Linting
npm run lint
npm run lint:fix

# Run web playground
npm install && npm run build && python3 playground/web/server.py
# Then open: http://localhost:8000/playground/web
```

### Blockly Playground Development
```bash
# From repository root
cd playground-blockly
npm install
npm run dev  # Development server with HMR
npm run build  # Production build
npm run preview  # Preview production build
```

### Running Tests
```bash
# Python tests - run specific test files directly
python universal_intelligence/community/agents/simple_agent/test.py
python universal_intelligence/community/models/local/qwen2_5_7b_instruct/test.py
python universal_intelligence/community/tools/simple_printer/test.py
```

## Architecture Overview

### Core Protocol Structure
The Universal Intelligence (UIN) protocol defines three fundamental building blocks:

1. **Universal Model** (`AbstractUniversalModel`): Self-contained AI model interfaces
   - Located in `universal_intelligence/core/universal_model.py`
   - Handles model loading, processing, and hardware optimization
   - Supports multiple engines (transformers, llama.cpp, mlx, web-llm)

2. **Universal Tool** (`AbstractUniversalTool`): Standardized tool interfaces
   - Located in `universal_intelligence/core/universal_tool.py`
   - Enables interaction with external systems and scripted tasks
   - All tool methods must return `tuple[Any, dict]` (result, logs)

3. **Universal Agent** (`AbstractUniversalAgent`): Composable AI agents
   - Located in `universal_intelligence/core/universal_agent.py`
   - Combines models, tools, and other agents
   - Supports dynamic tool/agent connections

### Community Components
Pre-built implementations are organized under `universal_intelligence/community/`:
- `models/`: Local and remote model implementations
  - `local/`: Hardware-optimized local models (auto-detects CUDA/MPS/CPU)
  - `remote/`: Cloud-based model integrations
- `tools/`: Ready-to-use tools (API caller, printer, MCP client)
- `agents/`: Agent implementations (simple_agent, default)

### Multi-Language Support
- Python implementation: `universal_intelligence/`
- TypeScript/JavaScript: `universal_intelligence/www/`
- Both implementations follow the same protocol specifications

### Key Design Patterns
1. **Contract-Based Design**: All components expose a `contract()` method describing their interface
2. **Tuple Returns**: All processing methods return `(result, logs)` for consistency
3. **Hardware Abstraction**: Models automatically optimize for available hardware
4. **Composability**: Agents can share models and dynamically connect tools/agents
5. **Configuration Flexibility**: While providing sensible defaults, all components support deep configuration

### Default Components
- Default Model: Qwen2.5-7B-Instruct (see `universal_intelligence/community/models/local/default/`)
- Default Agent: Simple Agent (see `universal_intelligence/community/agents/default/`)
- These can be imported directly: `from universal_intelligence import Model, Agent, Tool`

## Development Guidelines

1. **Testing**: Each component has its own `test.py` file - run these directly
2. **Linting**: Use `ruff` for Python (configured for 300 char lines) and ESLint for TypeScript
3. **Type Safety**: Python uses type hints; TypeScript uses strict mode
4. **Logging**: Use the Logger utility from `universal_intelligence.community.__utils__.logger`
5. **Model Support**: When adding models, include a `sources.yaml` for download URLs

## Blockly Playground Implementation

### Overview
The Blockly playground (`playground-blockly/`) provides a visual programming interface for Universal Intelligence using Google Blockly. It enables drag-and-drop composition of AI applications.

### Key Files
- `index.html`: Main interface with Blockly workspace and ES module imports
- `custom-blocks.js`: Block definitions and code generators for UIN components
- `app-web.js`: Application logic, workspace management, and code execution
- `logger.js`: Centralized Pino-based logging with browser compatibility
- `styles.css`: UI styling including modal and console output

### Important Implementation Details

#### 1. Tuple Return Handling
All UIN methods return `[result, logs]` tuples. Generated code must extract the result:
```javascript
result = (await model.process(input))[0];  // Extract result from tuple
```

#### 2. Browser Execution Pattern
Code runs in an async IIFE with global UIN components:
```javascript
(async function() {
  const Model = window.Model;
  const Agent = window.Agent;
  const Tool = window.Tool;
  // Generated code here
})()
```

#### 3. Tool Method Definition
Tools are created with method definitions on the instance:
```javascript
const tool = new Tool();
tool.methodName = async function(params) {
  // Implementation
  return [result, metadata];  // Must return tuple
};
```

#### 4. Agent Tool Usage
Agents need explicit instructions about available tools and how to use them:
```javascript
prompt = `You have access to:
- fetchData({url: "..."}) - Fetches URLs
- printText({text: "..."}) - Displays text
YOUR TASK: [specific instructions]`;
```

#### 5. Logger Configuration
The logger uses Pino with CSS-styled browser output:
- Located in `logger.js`
- Supports multiple arguments: `log.debug('func', 'arg:', value)`
- Color-coded levels: DEBUG (blue), INFO (green), WARN (orange), ERROR (red)

### Common Issues and Solutions

1. **Agent Not Using Tools**: Ensure the prompt explicitly instructs tool usage with method names and parameter formats
2. **Console Output Lost**: Check that outputConsole is properly capturing during execution
3. **Model Initialization Fails**: Add try-catch blocks and log the model object for debugging
4. **Generated Code Errors**: Use browser console to see full error stack traces

### Development Workflow
1. Make changes to blocks in `custom-blocks.js`
2. Test code generation in browser console
3. Update examples in `app-web.js` if needed
4. Ensure logger shows proper debug output
5. Update README.md with any new patterns