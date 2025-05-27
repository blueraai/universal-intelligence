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