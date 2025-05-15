# Universal Agents Project Memory

## Project Overview
- Implementing Universal Agents, a port of PocketFlow's functionality to Universal Intelligence framework
- Following a phased approach defined in docs/plans/plan-universal-agents-development-v1.0.0.md
- Completed all 4 phases of the implementation plan:
  1. Core Foundation (Node and Flow abstractions)
  2. Advanced Features (Batch and Async processing)
  3. Design Patterns (RAG, Map-Reduce, Multi-Agent, Workflow)
  4. Refinement (Visualization, Testing, Documentation)

## Implementation Status

### Completed
- Initial branch structure and documentation
- Core Node and Flow abstractions with lifecycle methods
- Universal Intelligence integration (models, tools, agents)
- Pattern implementations:
  - RAG (Retrieval Augmented Generation)
  - Map-Reduce for parallel processing
  - Multi-Agent collaboration
  - Workflow orchestration with conditional branching
- Flow visualization utilities
- Example applications demonstrating usage patterns
- Comprehensive test suite with direct tests
- Core methods for testing compatibility
  - `run` method on Node class for direct execution
  - Tests that don't require external dependencies

### Current Branch
- Working on feature branch `feat/universal-agents-poc`
- Last commit: Added standalone tests and Node.run method

### Implementation Insights
- Node class must include a `run` method for direct execution
- Flow class needs clear node traversal logic and error handling
- Universal Intelligence integration requires careful type handling
- Pattern implementations should be modular and composable
- Tests should be runnable without external dependencies

### Next Steps (Beyond Current Milestone)
1. Optional enhancements:
   - Additional pattern implementations
   - Documentation refinements
   - Performance optimizations
   - Web UI for flow editing
   - Flow serialization and loading

## File Structure
```
universal_agents/
├── __init__.py
├── flow.py          # Flow execution engine
├── node.py          # Base Node classes with run method
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

docs/examples/
├── universal_agents_basic.py
├── universal_agents_map_reduce.py
├── universal_agents_multi_agent.py
├── universal_agents_rag.py
└── universal_agents_workflow.py

tests/universal_agents/
├── __init__.py
├── direct_test.py   # Standalone tests without dependencies
├── patch_and_run.py # Test runner with runtime patching
├── test_batch_node.py
├── test_flow_basic.py
├── test_node_basic.py
├── test_pattern_implementations.py
├── test_universal_integration.py
└── test_visualization.py
```

## Key Features
1. **Core Abstractions**:
   - Node: Basic processing unit with prep/exec/post lifecycle and run method
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

6. **Testing**:
   - Comprehensive unit tests for all components
   - Standalone tests that don't require dependencies
   - Runtime patching for testing complex components

## Usage Examples
- Basic flow creation: universal_agents_basic.py
- RAG implementation: universal_agents_rag.py
- Parallel processing: universal_agents_map_reduce.py
- Agent collaboration: universal_agents_multi_agent.py
- Complex workflows: universal_agents_workflow.py

## Test Strategy
- Direct tests: Standalone tests that don't require external dependencies
- Integration tests: Tests that verify integration with Universal Intelligence components
- Pattern tests: Tests that verify pattern implementations
- Visualization tests: Tests for visualization utilities

## Milestone Achievement
The project has successfully reached its goal of implementing a full port of PocketFlow's flow-based execution model to work with Universal Intelligence components. The implementation includes all core features, advanced capabilities, design patterns, and supporting utilities as outlined in the development plan.

The addition of standalone tests ensures that the components work correctly without external dependencies, making the implementation more robust and easier to test.