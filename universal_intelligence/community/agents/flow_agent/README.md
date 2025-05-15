# Flow-based Universal Agent

A Universal Intelligence implementation of PocketFlow functionality.

## Overview

The Flow-based Universal Agent extends the Universal Agent interface with PocketFlow's flow-based execution model, enabling complex AI workflows through connected processing nodes.

## Key Components

- **FlowUniversalAgent**: Main agent class implementing the AbstractUniversalAgent interface
- **Node**: Base class for all processing nodes with prep/exec/post lifecycle
- **Flow**: Graph-based workflow manager connecting nodes through labeled actions
- **Specialized Variants**: BatchNode, AsyncNode, BatchFlow, AsyncFlow, etc.

## Getting Started

```python
from universal_intelligence.community.agents.flow_agent import FlowUniversalAgent
from universal_intelligence.community.agents.flow_agent.nodes import TextNode, LLMNode
from universal_intelligence.community.models.llama3_2_1b_instruct import UniversalModel

# Create an agent with a model
model = UniversalModel()
agent = FlowUniversalAgent(model=model)

# Create nodes
input_node = TextNode(name="input")
processing_node = LLMNode(name="processing", 
                          prompt="Summarize this text: {text}")
output_node = TextNode(name="output")

# Connect nodes
input_node - "next" >> processing_node
processing_node - "next" >> output_node

# Create flow
flow = agent.create_flow(start=input_node)

# Run the flow
result = agent.process(
    input="The Universal Intelligence framework provides a standardized way to work with AI models, tools, and agents.",
    flow=flow
)

print(result[0])  # Print the generated response
```

## Documentation

For detailed documentation, see:

- [Flow-based Agent Usage Guide](../../../docs/guides/guide-flow-based-agent-usage-v1.0.0.md)
- [Flow-based Agent Specification](../../../docs/specs/spec-flow-based-universal-agent-v1.0.0.md)
- [PocketFlow and Universal Intelligence Analysis](../../../docs/analysis/analysis-pocketflow-universal-intelligence-comparison-v1.0.0.md)

## Implementation Status

This component is under active development according to the [implementation plan](../../../docs/plans/plan-flow-based-agent-implementation-v1.0.0.md).