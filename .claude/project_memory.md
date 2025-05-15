# Universal Agents Project Memory

## Project Overview
- Implementing Universal Agents, a port of PocketFlow's functionality to Universal Intelligence framework
- Following a phased approach defined in docs/plans/plan-universal-agents-development-v1.0.0.md
- Completed Phase 3 (Design Patterns) and starting Phase 4 (Refinement and Documentation)

## Implementation Status

### Completed
- Initial branch structure and documentation
- Core Node and Flow abstractions
- Universal Intelligence integration (models, tools, agents)
- Pattern implementations:
  - RAG (Retrieval Augmented Generation)
  - Map-Reduce for parallel processing
  - Multi-Agent collaboration
  - Workflow orchestration with conditional branching
- Flow visualization utilities
- Example applications demonstrating usage patterns

### Current Branch
- Working on feature branch `feat/universal-agents-poc`
- Last commit: Added flow visualization utilities

### Next Steps (According to Development Plan)
1. Continue Phase 4 (Refinement and Documentation)
   - Performance optimization
   - Additional documentation
   - More comprehensive examples
   - Testing and validation

## File Structure
```
universal_agents/
├── __init__.py
├── flow.py          # Flow execution engine
├── node.py          # Base Node classes
├── visualization.py # Flow visualization utilities
├── patterns/        # Design pattern implementations
│   ├── __init__.py
│   ├── map_reduce.py
│   ├── multi_agent.py
│   ├── rag.py
│   └── workflow.py
└── universal_integration/  # UIN integration components
    ├── __init__.py
    ├── agent_node.py
    ├── model_node.py
    └── tool_node.py
```

## Examples
```
docs/examples/
├── universal_agents_basic.py
├── universal_agents_map_reduce.py
├── universal_agents_multi_agent.py
├── universal_agents_rag.py
└── universal_agents_workflow.py
```

## Key Features
1. **Core Abstractions**:
   - Node: Basic processing unit with prep/exec/post lifecycle
   - Flow: Orchestration engine for connected nodes
   - Pattern implementations: Ready-to-use workflow templates

2. **Node Types**:
   - BatchNode: For processing multiple items efficiently
   - AsyncNode: For non-blocking asynchronous operations
   - SpecializedNodes: For specific Universal Intelligence components

3. **Flow Capabilities**:
   - Shared state management for inter-node communication
   - Conditional branching with action-based routing
   - Error handling through special connections
   - Visualization for debugging and monitoring

4. **Pattern Implementations**:
   - RAG: Combining retrieval with generation
   - Map-Reduce: Parallel processing with aggregation
   - Multi-Agent: Collaborative problem-solving with specialist agents
   - Workflow: Complex conditional flows with decision points

5. **Visualization**:
   - Interactive HTML/D3.js visualizations
   - Flow structure rendering
   - Execution path tracing

## Usage Examples
- Basic flow creation: universal_agents_basic.py
- RAG implementation: universal_agents_rag.py
- Parallel processing: universal_agents_map_reduce.py
- Agent collaboration: universal_agents_multi_agent.py
- Complex workflows: universal_agents_workflow.py