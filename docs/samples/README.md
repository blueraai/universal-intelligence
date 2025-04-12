# Universal Intelligence Examples

This directory contains examples that demonstrate the capabilities and usage patterns of the Universal Intelligence framework. Each example is designed to showcase different aspects of the framework, from basic usage to advanced features.

## Examples Overview

| Example | Description | Key Concepts |
|---------|-------------|--------------|
| [basic_agent.py](basic_agent.py) | Demonstrates the simplest usage of Universal Intelligence | Model initialization, Agent creation, Basic processing |
| [tool_using_agent.py](tool_using_agent.py) | Shows how to create and use tools with agents | Tool creation, Tool configuration, Agent-tool integration |
| [multi_agent_system.py](multi_agent_system.py) | Illustrates how to create systems of collaborating agents | Model sharing, Agent specialization, Agent-to-agent communication |
| [rag_agent.py](rag_agent.py) | Demonstrates retrieval-augmented generation capabilities | Context provision, Document retrieval, Contextual processing |
| [specialized_agent.py](specialized_agent.py) | Shows how to create domain-specific agents | Model configuration, Domain-specific tools, Specialized processing |

## Running the Examples

To run these examples, you need to have the `universal-intelligence` package installed:

```bash
# For NVIDIA GPUs
pip install "universal-intelligence[community,cuda]"

# For Apple Silicon
pip install "universal-intelligence[community,mps]"

# For CPU-only systems
pip install "universal-intelligence[community]"
```

Once installed, you can run any example from the command line:

```bash
python basic_agent.py
```

## Usage Notes

1. **Hardware Detection**: The framework automatically detects and optimizes for your hardware. The examples will run on CUDA GPUs, Apple Silicon (MPS), or CPU with appropriate optimizations.

2. **Memory Management**: If you experience memory issues, you can adjust the `max_memory_allocation` parameter when creating models:

```python
model = Model(max_memory_allocation=0.6)  # Use up to 60% of available memory
```

3. **Model Selection**: By default, the examples use the standard model (Qwen2.5-7B-Instruct). You can specify a different model:

```python
from universal_intelligence.community.models.phi4 import UniversalModel as Phi4Model
model = Phi4Model()
```

4. **Engine Selection**: You can specify which engine to use:

```python
model = Model(engine="transformers")  # Force using transformers engine
```

5. **Quantization**: You can specify the quantization level:

```python
model = Model(quantization="BNB_4")  # Use 4-bit quantization
```

## Example Extensions

These examples can be extended in several ways:

1. **Custom Tools**: Create your own tools by implementing the `AbstractUniversalTool` class.

2. **Custom Agents**: Create specialized agents by implementing the `AbstractUniversalAgent` class.

3. **Custom Models**: Create model implementations by implementing the `AbstractUniversalModel` class.

4. **Integration with External Services**: Use MCP to integrate with external services.

## Additional Resources

For more detailed information about the Universal Intelligence framework, refer to the main documentation:

- [System Architecture](../00_system_architecture.md)
- [Overview](../01_overview.md)
- [Core Architecture](../02_core_architecture.md)
- [Plugin Architecture](../03_plugin_architecture.md)
