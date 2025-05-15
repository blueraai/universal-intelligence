"""Universal Agents - Multi-Agent Pattern Implementation

This module provides a ready-to-use implementation of the Multi-Agent pattern
using Universal Agents. The Multi-Agent pattern enables collaboration between
different specialized agents to solve complex problems.
"""
import logging
from typing import Any, Dict, List, Optional, Union, Callable, TypeVar, Generic, Tuple
from ..node import Node, Flow
from ..universal_integration import UniversalModelNode, UniversalToolNode, UniversalAgentNode
from universal_intelligence.core.universal_model import AbstractUniversalModel
from universal_intelligence.core.universal_tool import AbstractUniversalTool
from universal_intelligence.core.universal_agent import AbstractUniversalAgent

logger = logging.getLogger(__name__)
T = TypeVar('T')

class AgentCoordinatorNode(Node):
    """Node that coordinates the work of multiple specialized agents.
    
    The AgentCoordinatorNode distributes tasks to specialized agents and
    integrates their outputs, acting as the central coordination point in
    a multi-agent system.
    """
    
    def __init__(self, 
                 model: AbstractUniversalModel,
                 planning_prompt_template: str,
                 integration_prompt_template: str,
                 input_key: str = "user_input",
                 output_key: str = "final_response",
                 agent_outputs_key: str = "agent_outputs",
                 model_parameters: Optional[Dict[str, Any]] = None,
                 name: Optional[str] = None):
        """Initialize an AgentCoordinatorNode.
        
        Args:
            model: Universal Intelligence model for coordination
            planning_prompt_template: Template for planning agent interactions
            integration_prompt_template: Template for integrating agent outputs
            input_key: Key in shared state for input query/task
            output_key: Key in shared state to store final response
            agent_outputs_key: Key in shared state for agent outputs
            model_parameters: Optional parameters for the model
            name: Optional name for the node
        """
        super().__init__(name=name)
        self.model = model
        self.planning_prompt_template = planning_prompt_template
        self.integration_prompt_template = integration_prompt_template
        self.input_key = input_key
        self.output_key = output_key
        self.agent_outputs_key = agent_outputs_key
        self.model_parameters = model_parameters or {}
        self.connection_types = {}  # Maps action to agent type
    
    def register_agent(self, action: str, agent_type: str):
        """Register an agent type for a specific action.
        
        Args:
            action: The action name that triggers this agent
            agent_type: A descriptive name for the agent type
        """
        self.connection_types[action] = agent_type
        logger.info(f"Registered agent type '{agent_type}' for action '{action}'")
    
    def prep(self, shared: Dict[str, Any]) -> Dict[str, Any]:
        """Plan which agents to use based on the input.
        
        Args:
            shared: Shared state dictionary
            
        Returns:
            Planning data
        """
        if self.input_key not in shared:
            raise KeyError(f"Input key '{self.input_key}' not found in shared state")
        
        user_input = shared[self.input_key]
        
        # Create a prompt for planning
        agent_options = "\n".join([f"- {agent_type}" for agent_type in self.connection_types.values()])
        prompt = self.planning_prompt_template.format(
            user_input=user_input,
            agent_options=agent_options
        )
        
        # Remember original input for later integration
        return {
            "prompt": prompt,
            "user_input": user_input,
            "planning_phase": True
        }
    
    def exec(self, prep_data: Dict[str, Any]) -> str:
        """Execute the model for planning or integration.
        
        Args:
            prep_data: Prepared data
            
        Returns:
            Model output
        """
        return self.model.generate(prep_data["prompt"], **self.model_parameters)
    
    def post(self, shared: Dict[str, Any], prep_data: Dict[str, Any], exec_result: str) -> str:
        """Process model output and determine next action.
        
        Args:
            shared: Shared state dictionary
            prep_data: Prepared data
            exec_result: Model output
            
        Returns:
            Next action to take
        """
        if prep_data.get("planning_phase", False):
            # This was the planning phase, so determine which agent to use
            # Parse the model's output to decide
            # For simplicity, we'll use a simple approach here
            
            # Store the planning result for reference
            shared["coordination_plan"] = exec_result
            
            # Decide which agent to use based on the plan
            # In a real implementation, this would be more sophisticated
            # and might involve machine parsing of the model output
            for action, agent_type in self.connection_types.items():
                if agent_type.lower() in exec_result.lower():
                    logger.info(f"Selected agent type '{agent_type}' based on coordination plan")
                    # Initialize the agent outputs if not exists
                    if self.agent_outputs_key not in shared:
                        shared[self.agent_outputs_key] = {}
                    return action
            
            # If no specific agent was identified, use the default next action
            logger.info("No specific agent identified in plan, using default 'next' action")
            return "next"
        else:
            # This was the integration phase after agents have run
            shared[self.output_key] = exec_result
            return "complete"
    
    def handle_agent_return(self, shared: Dict[str, Any], agent_type: str) -> str:
        """Handle an agent's return and decide next steps.
        
        Args:
            shared: Shared state dictionary
            agent_type: The type of agent that just completed
            
        Returns:
            Next action to take
        """
        # Check if we've collected outputs from all expected agents
        agent_outputs = shared.get(self.agent_outputs_key, {})
        
        # Get the user input and agent outputs for integration
        user_input = shared[self.input_key]
        
        # Format the outputs for the model
        agent_outputs_text = "\n\n".join([
            f"=== {agent_type} ===\n{output}" 
            for agent_type, output in agent_outputs.items()
        ])
        
        # Create integration prompt
        prompt = self.integration_prompt_template.format(
            user_input=user_input,
            agent_outputs=agent_outputs_text
        )
        
        # Prepare for integration phase
        return {
            "prompt": prompt,
            "user_input": user_input,
            "planning_phase": False
        }


class SpecialistAgentNode(UniversalAgentNode):
    """Node that represents a specialist agent with a specific area of expertise.
    
    The SpecialistAgentNode executes a Universal Intelligence agent with
    appropriate context about its specialized role and expertise area.
    """
    
    def __init__(self, 
                 agent: AbstractUniversalAgent,
                 agent_type: str,
                 role_description: str,
                 input_key: str = "user_input",
                 output_key: str = "agent_outputs",
                 coordinator_action: str = "back_to_coordinator",
                 name: Optional[str] = None):
        """Initialize a SpecialistAgentNode.
        
        Args:
            agent: Universal Intelligence agent to use
            agent_type: Descriptive type of this agent
            role_description: Description of this agent's role and expertise
            input_key: Key in shared state for input query/task
            output_key: Key in shared state to store outputs
            coordinator_action: Action to return to coordinator
            name: Optional name for the node
        """
        super().__init__(
            agent=agent,
            input_key=input_key,
            output_key=f"specialist_output_{agent_type}",
            name=name or f"specialist_{agent_type}"
        )
        self.agent_type = agent_type
        self.role_description = role_description
        self.coordinator_action = coordinator_action
        self.outputs_key = output_key
    
    def prep(self, shared: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare input for the specialist agent.
        
        Args:
            shared: Shared state dictionary
            
        Returns:
            Data for agent execution
        """
        if self.input_key not in shared:
            raise KeyError(f"Input key '{self.input_key}' not found in shared state")
        
        user_input = shared[self.input_key]
        
        # Add role context to the input
        agent_input = f"""
        [ROLE: {self.agent_type} - {self.role_description}]
        
        USER QUERY: {user_input}
        
        Please respond with your specialist analysis based on your expertise.
        """
        
        return {
            "agent_input": agent_input,
            "user_input": user_input
        }
    
    def post(self, shared: Dict[str, Any], prep_data: Dict[str, Any], exec_result: str) -> str:
        """Store agent output and return to coordinator.
        
        Args:
            shared: Shared state dictionary
            prep_data: Prepared data
            exec_result: Agent output
            
        Returns:
            Next action to take
        """
        # Ensure the output has been stored by parent class
        super().post(shared, prep_data, exec_result)
        
        # Store the specialist output in the agent outputs collection
        if self.outputs_key not in shared:
            shared[self.outputs_key] = {}
        
        shared[self.outputs_key][self.agent_type] = exec_result
        
        return self.coordinator_action


def create_multi_agent_flow(
    coordinator_model: AbstractUniversalModel,
    specialist_agents: Dict[str, Tuple[AbstractUniversalAgent, str]],
    planning_prompt_template: Optional[str] = None,
    integration_prompt_template: Optional[str] = None,
    input_key: str = "user_input",
    output_key: str = "final_response",
    coordinator_parameters: Optional[Dict[str, Any]] = None,
    name: Optional[str] = None
) -> Flow:
    """Create a Multi-Agent flow with a coordinator and specialist agents.
    
    Args:
        coordinator_model: Model for the coordinator
        specialist_agents: Dictionary mapping agent types to (agent, description) tuples
        planning_prompt_template: Optional custom prompt for planning
        integration_prompt_template: Optional custom prompt for integration
        input_key: Key in shared state for input query/task
        output_key: Key in shared state to store final response
        coordinator_parameters: Optional parameters for the coordinator model
        name: Optional name for the flow
        
    Returns:
        Configured Multi-Agent flow
    """
    # Use default prompt templates if not provided
    if not planning_prompt_template:
        planning_prompt_template = """
        You are a coordinator for a team of specialized AI agents. Your task is to analyze
        the user's query and determine which specialist agent(s) should handle it.
        
        Available specialists:
        {agent_options}
        
        User query: {user_input}
        
        Analyze the query and determine which specialist(s) would be best suited to respond.
        Provide a brief explanation of your reasoning.
        """
    
    if not integration_prompt_template:
        integration_prompt_template = """
        You are a coordinator for a team of specialized AI agents. You've received outputs
        from different specialists regarding the user's query. Your task is to integrate
        these outputs into a cohesive, comprehensive response.
        
        User query: {user_input}
        
        Specialist outputs:
        {agent_outputs}
        
        Please synthesize these outputs into a unified, coherent response that addresses
        the user's query comprehensively. Be sure to credit information to the appropriate
        specialists and resolve any contradictions.
        """
    
    # Create the coordinator node
    coordinator = AgentCoordinatorNode(
        model=coordinator_model,
        planning_prompt_template=planning_prompt_template,
        integration_prompt_template=integration_prompt_template,
        input_key=input_key,
        output_key=output_key,
        model_parameters=coordinator_parameters,
        name="coordinator"
    )
    
    # Create and connect specialist agent nodes
    for agent_type, (agent, description) in specialist_agents.items():
        specialist = SpecialistAgentNode(
            agent=agent,
            agent_type=agent_type,
            role_description=description,
            input_key=input_key,
            name=f"specialist_{agent_type}"
        )
        
        # Connect coordinator to specialist
        coordinator - agent_type >> specialist
        
        # Connect specialist back to coordinator
        specialist - "back_to_coordinator" >> coordinator
        
        # Register agent type with coordinator
        coordinator.register_agent(agent_type, agent_type)
    
    # Create and return the flow
    return Flow(start=coordinator, name=name or "multi_agent_flow")