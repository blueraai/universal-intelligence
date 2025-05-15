"""Universal Agents - Workflow Example

This example demonstrates how to create and run Workflow patterns with Universal Agents,
enabling complex, conditional execution paths with decision points and branching.
"""

import logging
import sys
import os
from typing import List, Dict, Any, Tuple

# Add root to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from universal_agents.flow import Flow
from universal_agents.node import Node
from universal_agents.patterns.workflow import (
    DecisionNode,
    ModelDecisionNode,
    ParallelNode,
    SequentialWorkflowNode,
    LoopNode,
    create_conditional_workflow
)
from universal_agents.universal_integration import (
    UniversalModelNode,
    UniversalToolNode
)
from universal_intelligence.core.universal_model import AbstractUniversalModel
from universal_intelligence.community.models.default import get_default_model

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Sample data for demonstration
SAMPLE_QUERY = "What are the potential impacts of quantum computing on cryptography?"
RESEARCH_TOPICS = [
    "quantum computing basics",
    "current cryptographic standards",
    "quantum-resistant algorithms",
    "timeline for quantum threat"
]

# Prompt templates for different node types
DECISION_PROMPT_TEMPLATE = """
Analyze the user query and determine the most appropriate research approach.

User query: {query}

Based on the query, which approach would be most effective?
"""

RESEARCH_PROMPT_TEMPLATE = """
Research the following topic related to quantum computing and cryptography:

Topic: {topic}

Provide a concise summary of key points, current state, and future outlook.
"""

SYNTHESIS_PROMPT_TEMPLATE = """
Synthesize the following research findings into a cohesive response:

Query: {query}

Research findings:
{findings}

Provide a comprehensive answer to the query based on these findings.
"""


class SimpleTextProcessingNode(Node):
    """A simple node that processes text in some way."""
    
    def __init__(self, processor_fn, input_key, output_key, name=None):
        super().__init__(name=name)
        self.processor_fn = processor_fn
        self.input_key = input_key
        self.output_key = output_key
    
    def prep(self, shared):
        if self.input_key not in shared:
            raise KeyError(f"Input key '{self.input_key}' not found in shared state")
        return shared[self.input_key]
    
    def exec(self, prep_data):
        return self.processor_fn(prep_data)
    
    def post(self, shared, prep_data, exec_result):
        shared[self.output_key] = exec_result
        return "next"


def run_conditional_workflow_example():
    """Run an example of a conditional workflow based on query analysis."""
    logger.info("Starting Conditional Workflow example...")
    
    # Initialize the Universal Intelligence model
    model = get_default_model()
    logger.info(f"Using model: {model.__class__.__name__}")
    
    # Define text processing functions for different branches
    def in_depth_analysis(text):
        return f"IN-DEPTH ANALYSIS: Comprehensive examination of '{text}' with detailed perspectives"
    
    def quick_overview(text):
        return f"QUICK OVERVIEW: Key points about '{text}' with essential information"
    
    def technical_breakdown(text):
        return f"TECHNICAL BREAKDOWN: Detailed technical examination of '{text}' with implementation details"
    
    # Create nodes for each conditional branch
    in_depth_branch = [
        SimpleTextProcessingNode(
            processor_fn=in_depth_analysis,
            input_key="query",
            output_key="analysis",
            name="in_depth_node"
        )
    ]
    
    quick_branch = [
        SimpleTextProcessingNode(
            processor_fn=quick_overview,
            input_key="query",
            output_key="analysis",
            name="quick_overview_node"
        )
    ]
    
    technical_branch = [
        SimpleTextProcessingNode(
            processor_fn=technical_breakdown,
            input_key="query",
            output_key="analysis",
            name="technical_node"
        )
    ]
    
    # Define options for the conditional workflow
    options = {
        "in_depth": (in_depth_branch, "Detailed analysis with comprehensive coverage"),
        "quick": (quick_branch, "Brief overview of key points"),
        "technical": (technical_branch, "Technical details with implementation focus")
    }
    
    # Create a conditional workflow
    workflow = create_conditional_workflow(
        model=model,
        decision_prompt=DECISION_PROMPT_TEMPLATE,
        options=options,
        input_keys=["query"],
        output_key="result",
        name="query_analysis_workflow"
    )
    
    # Prepare shared state
    shared_state = {
        "query": SAMPLE_QUERY
    }
    
    # Run the workflow
    logger.info("Running Conditional Workflow...")
    result = workflow.run(shared=shared_state)
    
    # Display results
    logger.info("Conditional Workflow complete")
    logger.info(f"Decision: {result.get('decision', 'Unknown')}")
    logger.info("Analysis Result:")
    print("\n" + "-" * 80)
    print(result["result"])
    print("-" * 80 + "\n")
    
    return result


def run_research_workflow_example():
    """Run an example of a research workflow with parallel processing and synthesis."""
    logger.info("Starting Research Workflow example...")
    
    # Initialize the Universal Intelligence model
    model = get_default_model()
    logger.info(f"Using model: {model.__class__.__name__}")
    
    # Create research nodes for each topic
    research_flows = {}
    for topic in RESEARCH_TOPICS:
        # Create a research node
        research_node = UniversalModelNode(
            model=model,
            prompt_template=RESEARCH_PROMPT_TEMPLATE,
            input_keys=["topic"],
            output_key="research_result",
            name=f"research_{topic.replace(' ', '_')}"
        )
        
        # Create a flow for this topic
        topic_flow = Flow(start=research_node, name=f"research_flow_{topic.replace(' ', '_')}")
        research_flows[topic] = topic_flow
    
    # Create a parallel node for concurrent research
    parallel_research = ParallelNode(
        flows=research_flows,
        output_key="research_results",
        name="parallel_research"
    )
    
    # Create a node to combine research results
    def combine_research_results(parallel_results):
        all_findings = []
        for topic, result in parallel_results.items():
            if "research_result" in result:
                finding = f"--- {topic.upper()} ---\n{result['research_result']}"
                all_findings.append(finding)
        return "\n\n".join(all_findings)
    
    combiner_node = SimpleTextProcessingNode(
        processor_fn=combine_research_results,
        input_key="research_results",
        output_key="combined_findings",
        name="research_combiner"
    )
    
    # Create synthesis node
    synthesis_node = UniversalModelNode(
        model=model,
        prompt_template=SYNTHESIS_PROMPT_TEMPLATE,
        input_keys=["query", "findings"],
        mapping={"findings": "combined_findings"},
        output_key="final_answer",
        name="synthesis_node"
    )
    
    # Connect the nodes
    parallel_research - "next" >> combiner_node - "next" >> synthesis_node
    
    # Create the workflow
    workflow = Flow(start=parallel_research, name="research_workflow")
    
    # Prepare shared state
    shared_state = {
        "query": SAMPLE_QUERY,
        "topic": RESEARCH_TOPICS[0]  # Default topic, will be overridden in each flow
    }
    
    # Set each topic in the appropriate flow's shared state
    for i, topic in enumerate(RESEARCH_TOPICS):
        shared_state[f"topic_{i}"] = topic
    
    # Run the workflow
    logger.info("Running Research Workflow...")
    result = workflow.run(shared=shared_state)
    
    # Display results
    logger.info("Research Workflow complete")
    logger.info("Research Synthesis:")
    print("\n" + "-" * 80)
    print(result["final_answer"])
    print("-" * 80 + "\n")
    
    return result


def run_iterative_workflow_example():
    """Run an example of an iterative workflow that refines results over multiple iterations."""
    logger.info("Starting Iterative Workflow example...")
    
    # Initialize the Universal Intelligence model
    model = get_default_model()
    logger.info(f"Using model: {model.__class__.__name__}")
    
    # Create a node for initial draft
    initial_draft_node = UniversalModelNode(
        model=model,
        prompt_template="""
        Create an initial draft response to the following query:
        
        Query: {query}
        
        Provide a basic answer that can be refined in further iterations.
        """,
        input_keys=["query"],
        output_key="current_draft",
        name="initial_draft"
    )
    
    # Create a node for refining the draft
    refine_node = UniversalModelNode(
        model=model,
        prompt_template="""
        Refine the current draft to improve it. This is iteration {iteration}.
        
        Query: {query}
        Current draft:
        {current_draft}
        
        Improvement focus for this iteration:
        {improvement_focus}
        
        Provide an improved version of the draft incorporating these improvements.
        """,
        input_keys=["query", "current_draft", "iteration", "improvement_focus"],
        output_key="current_draft",  # Overwrite the current draft
        name="refine_draft"
    )
    
    # Create nodes for the refinement flow
    improvement_node = UniversalModelNode(
        model=model,
        prompt_template="""
        Analyze the current draft and suggest a focus area for improvement.
        
        Query: {query}
        Current draft:
        {current_draft}
        Iteration: {iteration}
        
        What aspect should be improved in the next iteration? Focus on a single area 
        such as clarity, completeness, accuracy, examples, etc.
        """,
        input_keys=["query", "current_draft", "iteration"],
        output_key="improvement_focus",
        name="identify_improvement"
    )
    
    # Connect improvement and refine nodes
    improvement_node - "next" >> refine_node
    
    # Create the refinement flow
    refinement_flow = Flow(start=improvement_node, name="refinement_flow")
    
    # Create a loop node
    def should_continue_loop(shared, iteration):
        # Stop after 3 iterations
        return iteration >= 3
    
    loop_node = LoopNode(
        flow=refinement_flow,
        condition_fn=should_continue_loop,
        max_iterations=3,
        iteration_key="iteration",
        result_key="refinement_history",
        name="refinement_loop"
    )
    
    # Connect initial draft to loop
    initial_draft_node - "next" >> loop_node
    
    # Create the workflow
    workflow = Flow(start=initial_draft_node, name="iterative_refinement_workflow")
    
    # Prepare shared state
    shared_state = {
        "query": SAMPLE_QUERY
    }
    
    # Run the workflow
    logger.info("Running Iterative Workflow...")
    result = workflow.run(shared=shared_state)
    
    # Display results
    logger.info("Iterative Workflow complete")
    logger.info("Final Draft:")
    print("\n" + "-" * 80)
    print(result["current_draft"])
    print("-" * 80 + "\n")
    
    # Show the evolution of the draft
    print("Draft Evolution:")
    for i, iteration_result in enumerate(result.get("refinement_history", [])):
        print(f"\nIteration {i+1} Improvement Focus:")
        print(iteration_result.get("improvement_focus", "Not available"))
    
    return result


if __name__ == "__main__":
    print("\n=== Running Conditional Workflow Example ===\n")
    run_conditional_workflow_example()
    
    print("\n=== Running Research Workflow Example ===\n")
    run_research_workflow_example()
    
    print("\n=== Running Iterative Workflow Example ===\n")
    run_iterative_workflow_example()