# Universal Agents Usage Guide

## Overview

Universal Agents is a port of PocketFlow's functionality utilizing Universal Intelligence (UIN). It enables you to build complex AI workflows using connected processing nodes while leveraging UIN's standardized components. This guide explains how to use Universal Agents to create and execute LLM workflows.

## Getting Started

### Installation

Install the Universal Agents package alongside Universal Intelligence:

```bash
pip install universal-intelligence
pip install universal-agents
```

### Basic Usage

Here's a simple example of creating a text processing workflow:

```python
from universal_agents import Node, Flow
from universal_agents.universal_integration import UniversalModelNode
from universal_intelligence.community.models.llama3_2_1b_instruct import UniversalModel

# Create a Universal Intelligence model
model = UniversalModel()

# Create nodes
input_node = Node(name="input")
processing_node = UniversalModelNode(
    model=model,
    prompt_template="Summarize the following text: {text}"
)
output_node = Node(name="output")

# Connect nodes
input_node - "next" >> processing_node
processing_node - "next" >> output_node

# Create a flow
flow = Flow(start=input_node)

# Initialize shared state
shared = {
    "text": "Universal Intelligence provides a standardized way to work with AI models, tools, and agents across different platforms."
}

# Run the flow
result = flow.run(shared)

print(result["summary"])  # Print the generated summary
```

## Creating Nodes

### Basic Node Structure

Nodes are the fundamental building blocks of a flow. Each node has three main methods:

- **prep**: Prepares data for execution
- **exec**: Executes the core functionality
- **post**: Processes results and determines the next action

```python
from universal_agents import Node

class CustomNode(Node):
    def prep(self, shared):
        # Prepare data from shared state
        data = shared.get("input_data")
        return data
        
    def exec(self, prep_data):
        # Process the data
        result = self._transform_data(prep_data)
        return result
        
    def post(self, shared, prep_data, exec_result):
        # Store result in shared state
        shared["processed_data"] = exec_result
        # Return next action
        return "success"
        
    def _transform_data(self, data):
        # Helper method for data transformation
        return data.upper()
```

### Integration with Universal Intelligence

Universal Agents provides special nodes for integrating with UIN components:

#### UniversalModelNode

For using Universal Intelligence models:

```python
from universal_agents.universal_integration import UniversalModelNode
from universal_intelligence.community.models.llama3_2_1b_instruct import UniversalModel

# Create a model node
model = UniversalModel()
model_node = UniversalModelNode(
    model=model,
    prompt_template="Question: {question}\nContext: {context}",
    input_keys=["question", "context"],
    output_key="answer"
)

# In the flow, this will:
# 1. Format a prompt using values from shared state
# 2. Process the prompt with the UIN model
# 3. Store the result in shared[output_key]
```

#### UniversalToolNode

For using Universal Intelligence tools:

```python
from universal_agents.universal_integration import UniversalToolNode
from universal_intelligence.community.tools.api_caller import UniversalTool

# Create a tool node
api_tool = UniversalTool()
tool_node = UniversalToolNode(
    tool=api_tool,
    method_name="call_api",
    arg_mapping={
        "url": "api_url",
        "params": "api_params"
    },
    result_key="api_response"
)

# In the flow, this will:
# 1. Map shared state values to tool arguments
# 2. Call the specified tool method
# 3. Store the result in shared[result_key]
```

#### UniversalAgentNode

For using other Universal Intelligence agents:

```python
from universal_agents.universal_integration import UniversalAgentNode
from universal_intelligence.community.agents.simple_agent import UniversalAgent

# Create an agent node
agent = UniversalAgent()
agent_node = UniversalAgentNode(
    agent=agent,
    input_key="agent_input",
    output_key="agent_output"
)

# In the flow, this will:
# 1. Get the input from shared[input_key]
# 2. Process it with the UIN agent
# 3. Store the result in shared[output_key]
```

## Creating Flows

### Connecting Nodes

Nodes are connected using labeled actions, forming a directed graph:

```python
# Method 1: Using operator syntax
input_node - "success" >> processing_node
input_node - "error" >> error_node
processing_node - "success" >> output_node
processing_node - "error" >> error_node

# Method 2: Using direct connection
input_node.connect("success", processing_node)
input_node.connect("error", error_node)
processing_node.connect("success", output_node)
processing_node.connect("error", error_node)

# Create a flow starting at input_node
flow = Flow(start=input_node)
```

### Shared State

Nodes communicate through a shared state dictionary that persists throughout flow execution:

```python
# Initialize shared state
initial_state = {
    "user_id": "user_123",
    "preferences": {"language": "en", "mode": "concise"},
    "input_text": "Process this text"
}

# Run flow with initial state
final_state = flow.run(initial_state)

# Access final state
print(final_state["processed_results"])
```

## Advanced Features

### BatchNodes for Parallel Processing

Process multiple items efficiently using BatchNodes:

```python
from universal_agents import BatchNode, BatchFlow

class DocumentProcessor(BatchNode):
    def batch_prep(self, shared, items):
        # Prepare each document
        return [self._prepare_document(item) for item in items]
        
    def batch_exec(self, prep_results):
        # Process each prepared document
        return [self._process_document(doc) for doc in prep_results]
        
    def batch_post(self, shared, prep_results, exec_results):
        # Store results and determine next action
        shared["processed_documents"] = exec_results
        return "success"
        
# Create and connect batch nodes
processor = DocumentProcessor()
processor - "success" >> next_node

# Create a batch flow
batch_flow = BatchFlow(start=processor)

# Run with documents
shared = {"documents": [doc1, doc2, doc3]}
result = batch_flow.batch_run(shared, shared["documents"])
```

### AsyncNodes for Non-blocking Operations

Handle asynchronous operations using AsyncNodes:

```python
from universal_agents import AsyncNode, AsyncFlow

class APIFetcher(AsyncNode):
    async def async_prep(self, shared):
        # Prepare API request
        return shared.get("query")
        
    async def async_exec(self, prep_data):
        # Make asynchronous API call
        return await self._fetch_api_data(prep_data)
        
    async def async_post(self, shared, prep_data, exec_result):
        # Store results
        shared["api_response"] = exec_result
        return "success"
        
# Create and connect async nodes
fetcher = APIFetcher()
fetcher - "success" >> processor

# Create an async flow
async_flow = AsyncFlow(start=fetcher)

# Run asynchronously
import asyncio
shared = {"query": "search term"}
result = asyncio.run(async_flow.async_run(shared))
```

### Flow Composition

Combine flows to create complex applications:

```python
from universal_agents import Flow, CompositeFlow

# Create individual flows
input_flow = Flow(start=input_node)
processing_flow = Flow(start=processing_node)
output_flow = Flow(start=output_node)

# Create a composite flow with connections
composite_flow = CompositeFlow(
    flows=[input_flow, processing_flow, output_flow],
    connections={
        input_flow: {"complete": processing_flow},
        processing_flow: {"complete": output_flow}
    }
)

# Run the composite flow
result = composite_flow.run(shared)
```

## Common Design Patterns

### RAG (Retrieval Augmented Generation)

```python
from universal_agents import Node, Flow
from universal_agents.universal_integration import UniversalModelNode, UniversalToolNode
from universal_intelligence.community.tools.vector_search import VectorSearchTool
from universal_intelligence.community.models.llama3_2_1b_instruct import UniversalModel

# Create nodes
query_node = Node(name="query")
retrieval_node = UniversalToolNode(
    tool=VectorSearchTool(),
    method_name="search",
    arg_mapping={"query": "user_query", "top_k": "retrieval_count"},
    result_key="retrieved_documents"
)
context_node = Node(name="context_builder")
generation_node = UniversalModelNode(
    model=UniversalModel(),
    prompt_template="""Answer based on the following context:
    {context}
    
    Question: {question}""",
    input_keys=["context", "question"],
    output_key="answer"
)

# Connect nodes
query_node - "retrieve" >> retrieval_node
retrieval_node - "build_context" >> context_node
context_node - "generate" >> generation_node

# Create RAG flow
rag_flow = Flow(start=query_node)
```

### Multi-Agent Collaboration

```python
from universal_agents import Node, Flow
from universal_agents.universal_integration import UniversalAgentNode
from universal_intelligence.community.agents.simple_agent import UniversalAgent

# Create specialized agent nodes
researcher = UniversalAgentNode(
    agent=UniversalAgent(configuration={"role": "researcher"}),
    input_key="research_request",
    output_key="research_results"
)
writer = UniversalAgentNode(
    agent=UniversalAgent(configuration={"role": "writer"}),
    input_key="writing_request",
    output_key="draft"
)
editor = UniversalAgentNode(
    agent=UniversalAgent(configuration={"role": "editor"}),
    input_key="editing_request",
    output_key="final_content"
)

# Create coordination nodes
task_router = Node(name="task_router")
research_to_writing = Node(name="research_to_writing")
writing_to_editing = Node(name="writing_to_editing")

# Connect nodes
task_router - "research" >> researcher
researcher - "complete" >> research_to_writing
research_to_writing - "write" >> writer
writer - "complete" >> writing_to_editing
writing_to_editing - "edit" >> editor

# Create collaboration flow
collaboration_flow = Flow(start=task_router)
```

### Map-Reduce Pattern

```python
from universal_agents import Node, BatchFlow, BatchNode
from universal_agents.universal_integration import UniversalModelNode
from universal_intelligence.community.models.llama3_2_1b_instruct import UniversalModel

# Create map node
class MapNode(BatchNode):
    def __init__(self):
        super().__init__(name="mapper")
        self.model = UniversalModel()
        
    def batch_prep(self, shared, items):
        return items
        
    def batch_exec(self, prep_results):
        # Process each document independently
        summaries = []
        for doc in prep_results:
            response, _ = self.model.process(f"Summarize this document: {doc}")
            summaries.append(response)
        return summaries
        
    def batch_post(self, shared, prep_results, exec_results):
        shared["mapped_results"] = exec_results
        return "reduce"

# Create reduce node
class ReduceNode(Node):
    def __init__(self):
        super().__init__(name="reducer")
        self.model = UniversalModel()
        
    def prep(self, shared):
        return shared["mapped_results"]
        
    def exec(self, prep_data):
        # Combine all summaries
        all_summaries = "\n".join([f"{i+1}. {s}" for i, s in enumerate(prep_data)])
        response, _ = self.model.process(
            f"Combine these summaries into a cohesive overview:\n{all_summaries}"
        )
        return response
        
    def post(self, shared, prep_data, exec_result):
        shared["final_summary"] = exec_result
        return "complete"

# Connect nodes
mapper = MapNode()
reducer = ReduceNode()
mapper - "reduce" >> reducer

# Create map-reduce flow
mapreduce_flow = BatchFlow(start=mapper)
```

## Best Practices

1. **Modularity**: Create reusable nodes for common operations
2. **Error Handling**: Add dedicated error handling paths in your flows
3. **State Management**: Use clear naming conventions for shared state keys
4. **Testing**: Test individual nodes before combining them into flows
5. **Documentation**: Document the purpose and expected inputs/outputs of each node

## Debugging Flows

To debug flow execution, enable flow visualization and logging:

```python
# Enable visualization
flow = Flow(
    start=start_node,
    visualization=True,
    visualization_path="./flow_visualizations/"
)

# Enable logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Run with step-by-step execution
result = flow.run(shared, step_by_step=True)
```

## Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| Node not receiving expected data | Check shared state keys and prep method |
| Flow stops unexpectedly | Verify all possible actions have corresponding connections |
| Memory usage grows over time | Clear unused data from shared state |
| Performance bottlenecks | Use BatchNodes for parallel processing |
| Infinite loops | Add max_steps configuration or cycle detection |

## Examples

See the following examples for common use cases:

- [Simple Chat Agent](../examples/universal_agents_chat.py)
- [RAG Implementation](../examples/universal_agents_rag.py)
- [Multi-Agent Collaboration](../examples/universal_agents_collaboration.py)
- [API Integration](../examples/universal_agents_api.py)

## Reference

- [Universal Agents Specification](../specs/spec-universal-agents-v1.0.0.md)
- [Universal Intelligence Documentation](../universal_intelligence/README.md)