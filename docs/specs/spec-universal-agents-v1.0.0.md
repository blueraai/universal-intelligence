# Universal Agents Specification

## Overview

This specification defines the architecture and implementation of Universal Agents, a port of PocketFlow's functionality utilizing Universal Intelligence (UIN). Universal Agents enables the construction of complex AI workflows using a directed graph of processing nodes with shared state management, while leveraging UIN's standardized components.

## Architectural Components

### 1. Core Abstractions

#### Node

The fundamental processing unit that handles a specific task within a workflow.

```python
class Node:
    """Base class for all nodes in a flow."""
    
    def prep(self, shared):
        """Prepare data for execution.
        
        Args:
            shared: Shared state dictionary
            
        Returns:
            Data to be passed to exec
        """
        return None
        
    def exec(self, prep_data):
        """Execute the core functionality of the node.
        
        Args:
            prep_data: Data prepared by the prep method
            
        Returns:
            Result of execution
        """
        return None
        
    def post(self, shared, prep_data, exec_result):
        """Process execution results and determine next action.
        
        Args:
            shared: Shared state dictionary
            prep_data: Data that was prepared
            exec_result: Result from execution
            
        Returns:
            Action name to determine next node
        """
        return None
```

#### Flow

A directed graph of Nodes connected by labeled edges (actions).

```python
class Flow:
    """A directed graph of connected nodes."""
    
    def __init__(self, start):
        """Initialize a new flow.
        
        Args:
            start: The starting node for the flow
        """
        self.start = start
        self.connections = {}
        
    def run(self, shared=None):
        """Run the flow starting from the start node.
        
        Args:
            shared: Initial shared state dictionary
            
        Returns:
            Final state after flow execution
        """
        # Implementation details
```

#### Specialized Variants

- **BatchNode / BatchFlow**: For processing batches of data
- **AsyncNode / AsyncFlow**: For handling asynchronous operations
- **AsyncBatchNode / AsyncBatchFlow**: For asynchronous batch processing

### 2. UIN Integration Components

#### UniversalModelNode

Node wrapper for Universal Intelligence models:

```python
class UniversalModelNode(Node):
    """Node for executing Universal Intelligence models."""
    
    def __init__(self, model=None, prompt_template=None):
        """Initialize with a UIN model.
        
        Args:
            model: A Universal Intelligence model
            prompt_template: Template for formatting prompts with shared state variables
        """
        self.model = model
        self.prompt_template = prompt_template
    
    def exec(self, prep_data):
        """Execute the model with the prepared data."""
        # Process using UIN model
```

#### UniversalToolNode

Node wrapper for Universal Intelligence tools:

```python
class UniversalToolNode(Node):
    """Node for executing Universal Intelligence tools."""
    
    def __init__(self, tool, method_name, arg_mapping=None):
        """Initialize with a UIN tool.
        
        Args:
            tool: A Universal Intelligence tool
            method_name: The tool method to call
            arg_mapping: Mapping from shared state keys to method arguments
        """
        self.tool = tool
        self.method_name = method_name
        self.arg_mapping = arg_mapping
    
    def exec(self, prep_data):
        """Execute the tool with the prepared data."""
        # Invoke UIN tool
```

#### UniversalAgentNode

Node wrapper for Universal Intelligence agents:

```python
class UniversalAgentNode(Node):
    """Node for executing Universal Intelligence agents."""
    
    def __init__(self, agent, input_key="input", output_key="output"):
        """Initialize with a UIN agent.
        
        Args:
            agent: A Universal Intelligence agent
            input_key: Key in shared state for agent input
            output_key: Key in shared state for agent output
        """
        self.agent = agent
        self.input_key = input_key
        self.output_key = output_key
    
    def exec(self, prep_data):
        """Execute the agent with the prepared data."""
        # Process using UIN agent
```

## Integration with Universal Intelligence

Universal Agents integrates with UIN in the following ways:

1. **Model Integration**: Universal Agents can leverage any UIN model through the UniversalModelNode
2. **Tool Integration**: UIN tools can be used directly in flows through the UniversalToolNode
3. **Agent Integration**: UIN agents can be incorporated into flows through the UniversalAgentNode
4. **Contract-Based Extensibility**: All components follow UIN's contract-based approach for interoperability

## State Management

Universal Agents maintains a shared state dictionary accessible to all nodes:

1. **Initialization**: Initial state can be provided when starting a flow
2. **Modification**: Nodes can read from and write to the shared state
3. **Persistence**: The final state is returned when the flow completes
4. **Scoping**: Sub-flows can have isolated state with inheritance from parent

## Error Handling

Universal Agents implements robust error handling:

1. **Node Errors**: Individual node failures are caught and can be handled
2. **Fallbacks**: Nodes can specify fallback actions when errors occur
3. **Timeouts**: Detection and handling of long-running operations
4. **Logging**: Comprehensive logging of flow execution for debugging

## Execution Model

Flow execution follows these steps:

1. Start at the designated start node
2. Call the node's `prep` method with shared state
3. Pass prep results to the node's `exec` method
4. Call the node's `post` method with shared state, prep results, and exec results
5. Determine the next action from the post method's return value
6. Transition to the next node based on the action and connections
7. Repeat until reaching an end node or maximum steps

## Implementation Considerations

1. **Compatibility**: Ensure smooth integration with existing UIN components
2. **Performance**: Optimize for efficient execution of complex workflows
3. **Memory Management**: Prevent memory leaks from long-running flows
4. **Extensibility**: Allow for custom node types and flow behaviors
5. **Serialization**: Support serializing/deserializing flows for storage and distribution

## Future Extensions

1. **Parallel Execution**: Support for executing multiple nodes concurrently
2. **Distributed Flows**: Distribute flow execution across multiple machines
3. **Visual Editor**: Graphical interface for creating and editing flows
4. **Flow Analytics**: Collect metrics and insights on flow execution

## References

- [Universal Intelligence Core Documentation](../reference/universal-intelligence/core)
- [PocketFlow Reference Implementation](../reference/PocketFlow)