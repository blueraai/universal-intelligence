# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Universal Intelligence (UIN) is a framework-less protocol that standardizes AI development through three core specifications:

1. **Universal Model** - A standard interface for AI models with automatic hardware adaptation
2. **Universal Tool** - A standard interface for tools usable by AI agents
3. **Universal Agent** - A composable agent interface for using models, tools, and other agents

The project supports both Python (cloud/desktop) and JavaScript/TypeScript (web/mobile) implementations.

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