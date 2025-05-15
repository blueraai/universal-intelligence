"""Universal Agents - A port of PocketFlow patterns utilizing Universal Intelligence.

Universal Agents provide a flow-based execution model for building complex AI applications with
connected processing nodes, leveraging the standardized Universal Intelligence components.

Core abstractions:
- Node: Basic processing unit with prep/exec/post lifecycle
- Flow: Orchestration engine for connected nodes
- Patterns: Ready-to-use implementations of common design patterns

Universal Agents supports various flow patterns including:
- RAG (Retrieval Augmented Generation)
- Map-Reduce for parallel processing
- Multi-Agent collaborative systems
- Complex workflows with conditional branching
"""

from .node import Node, BatchNode, AsyncNode, AsyncBatchNode
from .flow import Flow, BatchFlow, AsyncFlow, AsyncBatchFlow
from .universal_integration import UniversalModelNode, UniversalToolNode, UniversalAgentNode
from .visualization import generate_flow_visualization, visualize_execution_path

__version__ = "0.1.0"

__all__ = [
    "Node",
    "BatchNode", 
    "AsyncNode",
    "AsyncBatchNode",
    "Flow",
    "BatchFlow", 
    "AsyncFlow",
    "AsyncBatchFlow",
    "UniversalModelNode",
    "UniversalToolNode",
    "UniversalAgentNode",
    "generate_flow_visualization",
    "visualize_execution_path"
]