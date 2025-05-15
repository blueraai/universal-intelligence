"""Universal Agents - Pattern Implementations

This module provides ready-to-use implementations of common design patterns
using Universal Agents flows.
"""

from .rag import create_rag_flow
from .map_reduce import (
    MapNode, ModelMapNode, 
    ReduceNode, ModelReduceNode,
    create_map_reduce_flow
)
from .multi_agent import (
    AgentCoordinatorNode,
    SpecialistAgentNode,
    create_multi_agent_flow
)
from .workflow import (
    DecisionNode,
    ModelDecisionNode,
    ParallelNode,
    SequentialWorkflowNode,
    LoopNode,
    create_conditional_workflow
)

__all__ = [
    "create_rag_flow",
    "MapNode",
    "ModelMapNode",
    "ReduceNode",
    "ModelReduceNode",
    "create_map_reduce_flow",
    "AgentCoordinatorNode",
    "SpecialistAgentNode",
    "create_multi_agent_flow",
    "DecisionNode",
    "ModelDecisionNode",
    "ParallelNode",
    "SequentialWorkflowNode",
    "LoopNode",
    "create_conditional_workflow"
]