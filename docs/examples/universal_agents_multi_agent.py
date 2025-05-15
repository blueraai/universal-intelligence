"""Universal Agents - Multi-Agent Example

This example demonstrates how to create and run a Multi-Agent flow with Universal Agents,
using Universal Intelligence agents for collaborative problem solving.
"""

import logging
import sys
import os
from typing import List, Dict, Any, Tuple

# Add root to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from universal_agents.flow import Flow
from universal_agents.patterns.multi_agent import (
    AgentCoordinatorNode, 
    SpecialistAgentNode,
    create_multi_agent_flow
)
from universal_intelligence.core.universal_agent import AbstractUniversalAgent
from universal_intelligence.core.universal_model import AbstractUniversalModel
from universal_intelligence.community.models.default import get_default_model
from universal_intelligence.community.agents.simple_agent import SimpleAgent
from universal_intelligence.core.utils.types import Message

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Define specialized agent prompts
RESEARCH_AGENT_PROMPT = """You are a specialized research agent. Your role is to find and summarize key facts, studies, and information
related to the user's query. Focus on providing well-researched, factual information with proper context."""

CREATIVE_AGENT_PROMPT = """You are a specialized creative agent. Your role is to provide innovative ideas, 
creative solutions, and think outside the box for the user's query. Consider unconventional approaches
and novel perspectives."""

CRITICAL_AGENT_PROMPT = """You are a specialized critical thinking agent. Your role is to evaluate 
ideas critically, identify potential issues, challenges, and logical flaws. Consider counter-arguments,
edge cases, and alternative perspectives for a balanced analysis."""

# Sample queries for demonstration
SAMPLE_QUERIES = [
    "What are effective strategies for reducing plastic waste in urban environments?",
    "How might artificial intelligence impact job markets over the next decade?",
    "What are the most promising renewable energy technologies for addressing climate change?",
]


def create_specialized_agent(model: AbstractUniversalModel, system_prompt: str) -> AbstractUniversalAgent:
    """Create a specialized agent with a particular system prompt.
    
    Args:
        model: The Universal Intelligence model to use
        system_prompt: System prompt defining the agent's role
        
    Returns:
        Configured specialized agent
    """
    agent = SimpleAgent()
    agent.load(
        model=model,
        system_prompt=system_prompt
    )
    return agent


def run_multi_agent_example(query_index: int = 0):
    """Run a complete multi-agent example using Universal Agents.
    
    Args:
        query_index: Index of the sample query to use
    """
    logger.info("Starting Multi-Agent example...")
    
    # Initialize the Universal Intelligence model
    model = get_default_model()
    logger.info(f"Using model: {model.__class__.__name__}")
    
    # Create specialized agents
    research_agent = create_specialized_agent(model, RESEARCH_AGENT_PROMPT)
    creative_agent = create_specialized_agent(model, CREATIVE_AGENT_PROMPT)
    critical_agent = create_specialized_agent(model, CRITICAL_AGENT_PROMPT)
    
    # Define specialist agents with descriptions
    specialist_agents = {
        "research": (research_agent, "Provides factual information and research-based insights"),
        "creative": (creative_agent, "Generates innovative ideas and unconventional approaches"),
        "critical": (critical_agent, "Evaluates concepts critically and identifies challenges")
    }
    
    # Create multi-agent flow
    flow = create_multi_agent_flow(
        coordinator_model=model,
        specialist_agents=specialist_agents,
        name="collaborative_problem_solving"
    )
    
    # Get the query to process
    query = SAMPLE_QUERIES[query_index % len(SAMPLE_QUERIES)]
    logger.info(f"Processing query: {query}")
    
    # Prepare shared state with input query
    shared_state = {
        "user_input": query
    }
    
    # Run the flow
    logger.info("Running Multi-Agent flow...")
    result = flow.run(shared=shared_state)
    
    # Display results
    logger.info("Multi-Agent flow complete")
    logger.info("Collaborative Response:")
    print("\n" + "-" * 80)
    print(result["final_response"])
    print("-" * 80 + "\n")
    
    # Display individual agent contributions
    print("Individual Agent Contributions:")
    for agent_type, contribution in result.get("agent_outputs", {}).items():
        print(f"\n--- {agent_type.upper()} AGENT ---")
        print(contribution[:500] + "..." if len(contribution) > 500 else contribution)
    
    # Return the result for potential further use
    return result


def run_custom_multi_agent_example():
    """Run a custom multi-agent example with manually created nodes."""
    logger.info("Starting custom Multi-Agent example...")
    
    # Initialize the Universal Intelligence model
    model = get_default_model()
    logger.info(f"Using model: {model.__class__.__name__}")
    
    # Custom planning prompt with more detailed instructions
    planning_prompt = """
    You are the lead coordinator for a team of AI specialists. Given a user query,
    your job is to determine which specialists would best contribute to solving it.
    
    Available specialists:
    {agent_options}
    
    User query: {user_input}
    
    Instructions:
    1. Analyze the query's domain, complexity, and required expertise
    2. Identify which specialist(s) would provide the most valuable insights
    3. Explain your selection strategy
    4. Provide specific questions or aspects each chosen specialist should address
    
    Your plan:
    """
    
    # Custom integration prompt with more structure
    integration_prompt = """
    You are the lead coordinator synthesizing insights from multiple AI specialists.
    
    User query: {user_input}
    
    Specialist contributions:
    {agent_outputs}
    
    Instructions for synthesis:
    1. Identify key insights from each specialist
    2. Note areas of consensus and disagreement
    3. Evaluate the quality and relevance of each contribution
    4. Create a comprehensive response that:
       - Provides a clear, direct answer to the user query
       - Integrates the most valuable insights from each specialist
       - Acknowledges limitations or areas of uncertainty
       - Suggests next steps or additional considerations
    
    Your integrated response:
    """
    
    # Create specialized agents
    research_agent = create_specialized_agent(model, RESEARCH_AGENT_PROMPT)
    creative_agent = create_specialized_agent(model, CREATIVE_AGENT_PROMPT)
    critical_agent = create_specialized_agent(model, CRITICAL_AGENT_PROMPT)
    
    # Create coordinator
    coordinator = AgentCoordinatorNode(
        model=model,
        planning_prompt_template=planning_prompt,
        integration_prompt_template=integration_prompt,
        name="enhanced_coordinator"
    )
    
    # Create specialist nodes
    research_specialist = SpecialistAgentNode(
        agent=research_agent,
        agent_type="research",
        role_description="Expert in gathering and synthesizing factual information and research data",
        name="research_specialist"
    )
    
    creative_specialist = SpecialistAgentNode(
        agent=creative_agent,
        agent_type="creative",
        role_description="Expert in generating novel ideas and innovative approaches",
        name="creative_specialist"
    )
    
    critical_specialist = SpecialistAgentNode(
        agent=critical_agent,
        agent_type="critical",
        role_description="Expert in critical analysis, evaluation, and identifying challenges",
        name="critical_specialist"
    )
    
    # Register agent types with coordinator
    coordinator.register_agent("research", "research")
    coordinator.register_agent("creative", "creative")
    coordinator.register_agent("critical", "critical")
    
    # Connect coordinator to specialists
    coordinator - "research" >> research_specialist
    coordinator - "creative" >> creative_specialist
    coordinator - "critical" >> critical_specialist
    
    # Connect specialists back to coordinator
    research_specialist - "back_to_coordinator" >> coordinator
    creative_specialist - "back_to_coordinator" >> coordinator
    critical_specialist - "back_to_coordinator" >> coordinator
    
    # Create flow
    flow = Flow(start=coordinator, name="custom_collaborative_problem_solving")
    
    # Get a query to process
    query = "How can we redesign urban transportation systems to be more sustainable and efficient?"
    logger.info(f"Processing query: {query}")
    
    # Prepare shared state with input query
    shared_state = {
        "user_input": query
    }
    
    # Run the flow
    logger.info("Running custom Multi-Agent flow...")
    result = flow.run(shared=shared_state)
    
    # Display results
    logger.info("Custom Multi-Agent flow complete")
    logger.info("Collaborative Response:")
    print("\n" + "-" * 80)
    print(result["final_response"])
    print("-" * 80 + "\n")
    
    # Return the result for potential further use
    return result


if __name__ == "__main__":
    print("\n=== Running Multi-Agent Example ===\n")
    run_multi_agent_example()
    
    print("\n=== Running Custom Multi-Agent Example ===\n")
    run_custom_multi_agent_example()