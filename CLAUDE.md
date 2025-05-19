# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Universal Intelligence (UIN) is a framework-less protocol that standardizes AI development through three core specifications:

1. **Universal Model** - A standard interface for AI models with automatic hardware adaptation
2. **Universal Tool** - A standard interface for tools usable by AI agents
3. **Universal Agent** - A composable agent interface for using models, tools, and other agents

The project supports both Python (cloud/desktop) and JavaScript/TypeScript (web/mobile) implementations.

## Current Work: Blockly Integration (May 15, 2025)

### Status: Phase 1 - Core Implementation (In Progress)

Working on integrating Google's Blockly visual programming editor with the Universal Agents framework. Currently debugging code generator registration issues.

### Current Issue
Blockly blocks load correctly but JavaScript/Python generators fail with error:
```
Uncaught Error: JavaScript generator does not know how to generate code for block type "universal_agents_node"
```

### Project Structure
```
docs/examples/blockly-integration/
├── index.html                      # Main demo interface (has generator errors)
├── index_fixed.html               # Attempted fix with proper script loading
├── basic_node_block_definition.js  # Universal Agents Node block
├── flow_block_definition.js        # Flow block definition
├── model_node_block_definition.js  # Model node block
├── toolbox_configuration.js        # Minimal toolbox config
├── server.py                       # Demo server with CORS support
├── test.js                        # Browser integration tests
├── validate_blocks.py             # Python validation script
├── debug_blockly.html             # Step-by-step debugging page
└── check_generators.html          # Generator testing page
```

### Key Commands
```bash
# Run the demo server
python run_blockly_demo.py

# Run validation tests
python run_blockly_demo.py --tests

# Access the demo
http://localhost:8000/index.html
http://localhost:8000/index_fixed.html
```

### Technical Details

**Environment:**
- Blockly version: 12.0.0
- Browser: Chrome/Safari on macOS
- Server: Python HTTP server on port 8000

**Error Details:**
1. Block definitions load successfully
2. Generators are defined but not registered properly
3. Error occurs in updateCode() when calling Blockly.JavaScript.workspaceToCode()
4. See `localhost-1747612346522.log` for full console output

**Failed Attempts:**
1. Moving script loading to window.onload
2. Creating headless integration tests (ES module conflicts)
3. Reordering script includes
4. Adding explicit generator registration
5. Creating fixed HTML with proper load order

### Next Steps

1. **Debug Generator Registration (Priority: High)**
   - Check Blockly v12 breaking changes
   - Test with minimal example
   - Compare with Blockly documentation examples
   - Consider downgrading to Blockly v11 if needed

2. **Fix Script Loading Order (Priority: High)**
   - Ensure blocks are defined before workspace init
   - Verify generators are attached to Blockly namespace
   - Add console logging for initialization sequence

3. **Test Alternative Approaches (Priority: Medium)**
   - Try defining generators inline with blocks
   - Use Blockly's plugin system
   - Check if we need registerGenerator() calls

4. **Complete Phase 1 Implementation (Priority: Medium)**
   - Fix all three block types (Node, Flow, ModelNode)
   - Implement proper code generation
   - Add connection logic between blocks
   - Create working example flows

### Phase Plan (from docs/plans/plan-blockly-integration-v1.0.0.md)

**Phase 1: Core Implementation** (Current)
- ✅ Block definitions for Node, Flow, ModelNode
- ❌ Code generation (blocked by generator errors)
- ✅ Basic UI integration
- ✅ Toolbox configuration

**Phase 2: Pattern Implementation** (Next)
- Pattern blocks (RAG, Map-Reduce, Multi-Agent)
- Universal Intelligence integration
- Advanced flow features
- Enhanced UI

**Phase 3: Runtime and Debugging** (Future)
- Live execution
- Debugging tools
- State visualization
- Persistence

**Phase 4: Advanced Features** (Future)
- Block factory
- Performance optimization
- External integrations
- Documentation

### Important Files for Debugging

1. `blockly-test-errors-1.png` - Screenshot of browser errors
2. `localhost-1747612346522.log` - Full console log with error traces
3. `integration_test.mjs` - Failed headless test attempt
4. Block definition files - Check generator function syntax

### MCP Integration Note

MCP tools are not currently configured. Future work includes:
- Setting up MCP puppeteer for automated browser testing
- Implementing time server demo (`time_server.py`)
- Testing with `test_time_mcp.py`

## Development Environment Setup

```bash
# Create and activate conda environment
conda create -n universal-intelligence python=3.10.16 -y
conda activate universal-intelligence

# Install dependencies based on hardware
pip install -r requirements.txt
pip install -r requirements-community.txt
pip install -r requirements-dev.txt

# For Apple Silicon
pip install -r requirements-mps.txt

# For NVIDIA GPUs
pip install -r requirements-cuda.txt

# For MCP support
pip install -r requirements-mcp.txt

# Install pre-commit hooks
pre-commit install
```

## Common Commands

### Testing

```bash
# Test a specific model implementation
python -m universal_intelligence.community.models.<model_name>.test

# Test a specific tool implementation
python -m universal_intelligence.community.tools.<tool_name>.test

# Test a specific agent implementation
python -m universal_intelligence.community.agents.<agent_name>.test

# Run playground example
python -m playground.example
```

### Linting

```bash
# Run all pre-commit hooks (includes linting)
pre-commit run --all-files
```

## Code Architecture

### Core Protocol (universal_intelligence/core/)

- `universal_model.py` - Base class and interface for AI models
- `universal_tool.py` - Base class and interface for tools
- `universal_agent.py` - Base class and interface for agents
- `utils/types.py` - Common type definitions

### Community Components (universal_intelligence/community/)

- **Models**: Pre-configured implementations of popular LLMs (Llama, Gemma, Qwen, etc.)
- **Tools**: Utility implementations like API callers and error handlers
- **Agents**: Agent implementations that compose models and tools

### Web Implementation (universal_intelligence/www/)

TypeScript implementation of the protocol for web environments, mirroring the Python structure.

## Component Development Guidelines

### Creating a New Model

1. Create a directory in `universal_intelligence/community/models/<model_name>/`
2. Implement the model in `model.py` by extending `AbstractUniversalModel`
3. Define model sources in `sources.yaml`
4. Add tests in `test.py` using the testing utilities

### Creating a New Tool

1. Create a directory in `universal_intelligence/community/tools/<tool_name>/`
2. Implement the tool in `tool.py` by extending `AbstractUniversalTool`
3. Add tests in `test.py` using the testing utilities

### Creating a New Agent

1. Create a directory in `universal_intelligence/community/agents/<agent_name>/`
2. Implement the agent in `agent.py` by extending `AbstractUniversalAgent`
3. Add tests in `test.py` using the testing utilities

## Recommendations for Development

- Use the mixins in `universal_intelligence/community/<component>/__utils__/mixins/` to accelerate development
- Follow the pattern of existing implementations when creating new components
- Ensure backward compatibility when modifying core interfaces
- Run tests for any components you modify before committing changes

## Ethical Development Guidelines

- *ALWAYS* fix dependency issues and *NEVER* change functionality or deviate from specifications in order to satisfy broken tests, which completely invalidates their use and the effort in having them at all.