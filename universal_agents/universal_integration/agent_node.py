"""Universal Agents - Universal Agent Integration

This module provides nodes for integrating Universal Intelligence agents
into Universal Agents workflows.
"""

import logging
from typing import Any, Dict, List, Optional, Union, Callable

from ..node import Node, AsyncNode
from universal_intelligence.core.universal_agent import AbstractUniversalAgent

logger = logging.getLogger(__name__)


class UniversalAgentNode(Node):
    """Node for executing Universal Intelligence agents.
    
    This node enables the use of any Universal Intelligence agent within a flow.
    It handles input preparation, agent execution, and output processing.
    """
    
    def __init__(self, agent: AbstractUniversalAgent, 
                 input_key: str = "input",
                 context_key: Optional[str] = None,
                 output_key: str = "agent_output",
                 name: Optional[str] = None,
                 configuration: Optional[Dict[str, Any]] = None,
                 remember: bool = False,
                 stream: bool = False,
                 keep_alive: bool = True,
                 error_handling: str = "continue"):
        """Initialize a new Universal Agent node.
        
        Args:
            agent: A Universal Intelligence agent instance
            input_key: Key in shared state for agent input
            context_key: Optional key in shared state for context
            output_key: Key to store the agent output in shared state
            name: Optional name for the node
            configuration: Optional configuration for agent processing
            remember: Whether to remember this interaction in agent history
            stream: Whether to stream output asynchronously
            keep_alive: Whether to keep the model loaded for faster consecutive interactions
            error_handling: How to handle errors ('continue', 'raise', or 'return')
        """
        super().__init__(name or f"{agent.__class__.__name__}Node")
        self.agent = agent
        self.input_key = input_key
        self.context_key = context_key
        self.output_key = output_key
        self.configuration = configuration or {}
        self.remember = remember
        self.stream = stream
        self.keep_alive = keep_alive
        self.error_handling = error_handling
        
    def prep(self, shared: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare input for the agent.
        
        This method extracts input and optional context from shared state
        for processing by the agent.
        
        Args:
            shared: The shared state dictionary
            
        Returns:
            Dictionary with input and context data
        """
        # Extract input from shared state
        if self.input_key not in shared:
            logger.warning(f"Input key '{self.input_key}' not found in shared state")
            agent_input = ""
        else:
            agent_input = shared[self.input_key]
            
        # Extract context if specified
        context = None
        if self.context_key and self.context_key in shared:
            context = shared[self.context_key]
            
        # Get any extra tools or agents from shared state
        extra_tools = shared.get("extra_tools", [])
        extra_team = shared.get("extra_agents", [])
        
        # Get any additional configuration
        runtime_config = shared.get("agent_configuration", {})
        
        # Merge with node configuration
        config = {**self.configuration, **runtime_config}
        
        return {
            "input": agent_input,
            "context": context,
            "configuration": config,
            "extra_tools": extra_tools,
            "extra_team": extra_team
        }
        
    def exec(self, prep_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent with the prepared input.
        
        This method processes the prepared input with the agent
        and returns the agent's response.
        
        Args:
            prep_data: Dictionary with input and context data
            
        Returns:
            Dictionary with agent output and logs
        """
        try:
            # Process the input with the agent
            response, logs = self.agent.process(
                input=prep_data["input"],
                context=prep_data["context"],
                configuration=prep_data["configuration"],
                remember=self.remember,
                stream=self.stream,
                extra_tools=prep_data["extra_tools"],
                extra_team=prep_data["extra_team"],
                keep_alive=self.keep_alive
            )
            
            return {
                "response": response,
                "logs": logs,
                "success": True,
                "error": None
            }
            
        except Exception as e:
            logger.error(f"Error processing input with agent: {str(e)}")
            
            if self.error_handling == "raise":
                raise
            
            return {
                "response": f"Error: {str(e)}",
                "logs": {},
                "success": False,
                "error": str(e)
            }
        
    def post(self, shared: Dict[str, Any], prep_data: Dict[str, Any], exec_result: Dict[str, Any]) -> str:
        """Store the agent output in shared state.
        
        This method updates the shared state with the agent output
        and returns the next action based on success or failure.
        
        Args:
            shared: The shared state dictionary
            prep_data: Dictionary with input and context data
            exec_result: Dictionary with agent output and logs
            
        Returns:
            Next action to execute
        """
        # Store the agent response in shared state
        shared[self.output_key] = exec_result["response"]
        
        # Also store logs and status
        shared[f"{self.output_key}_logs"] = exec_result["logs"]
        shared[f"{self.output_key}_success"] = exec_result["success"]
        
        if exec_result["error"]:
            shared[f"{self.output_key}_error"] = exec_result["error"]
            return "error" if "error" in self.connections else "next"
        
        return "success" if "success" in self.connections else "next"


class AsyncUniversalAgentNode(AsyncNode, UniversalAgentNode):
    """Asynchronous node for executing Universal Intelligence agents.
    
    This node provides the same functionality as UniversalAgentNode,
    but supports asynchronous execution and streaming.
    """
    
    def __init__(self, agent: AbstractUniversalAgent, 
                 input_key: str = "input",
                 context_key: Optional[str] = None,
                 output_key: str = "agent_output",
                 name: Optional[str] = None,
                 configuration: Optional[Dict[str, Any]] = None,
                 remember: bool = False,
                 stream: bool = True,
                 keep_alive: bool = True,
                 error_handling: str = "continue",
                 stream_handler: Optional[Callable[[str], None]] = None):
        """Initialize a new Async Universal Agent node.
        
        Args:
            agent: A Universal Intelligence agent instance
            input_key: Key in shared state for agent input
            context_key: Optional key in shared state for context
            output_key: Key to store the agent output in shared state
            name: Optional name for the node
            configuration: Optional configuration for agent processing
            remember: Whether to remember this interaction in agent history
            stream: Whether to stream output asynchronously
            keep_alive: Whether to keep the model loaded for faster consecutive interactions
            error_handling: How to handle errors ('continue', 'raise', or 'return')
            stream_handler: Optional callback function for handling streaming output
        """
        UniversalAgentNode.__init__(
            self,
            agent=agent,
            input_key=input_key,
            context_key=context_key,
            output_key=output_key,
            name=name or f"Async{agent.__class__.__name__}Node",
            configuration=configuration,
            remember=remember,
            stream=stream,
            keep_alive=keep_alive,
            error_handling=error_handling
        )
        self.stream_handler = stream_handler
        
    async def async_exec(self, prep_data: Dict[str, Any]) -> Dict[str, Any]:
        """Asynchronously execute the agent with the prepared input.
        
        This method processes the prepared input with the agent
        and returns the agent's response, supporting streaming output.
        
        Args:
            prep_data: Dictionary with input and context data
            
        Returns:
            Dictionary with agent output and logs
        """
        try:
            if self.stream and self.stream_handler:
                # For streaming with handler, accumulate the output
                accumulated_output = []
                
                def stream_callback(chunk):
                    accumulated_output.append(chunk)
                    self.stream_handler(chunk)
                
                # Process with streaming
                response, logs = self.agent.process(
                    input=prep_data["input"],
                    context=prep_data["context"],
                    configuration=prep_data["configuration"],
                    remember=self.remember,
                    stream=True,
                    streaming_callback=stream_callback,
                    extra_tools=prep_data["extra_tools"],
                    extra_team=prep_data["extra_team"],
                    keep_alive=self.keep_alive
                )
                
                # Use accumulated output if available
                if accumulated_output:
                    response = "".join(accumulated_output)
            else:
                # Regular processing without streaming handler
                response, logs = self.agent.process(
                    input=prep_data["input"],
                    context=prep_data["context"],
                    configuration=prep_data["configuration"],
                    remember=self.remember,
                    stream=self.stream,
                    extra_tools=prep_data["extra_tools"],
                    extra_team=prep_data["extra_team"],
                    keep_alive=self.keep_alive
                )
            
            return {
                "response": response,
                "logs": logs,
                "success": True,
                "error": None
            }
            
        except Exception as e:
            logger.error(f"Error processing input with agent: {str(e)}")
            
            if self.error_handling == "raise":
                raise
            
            return {
                "response": f"Error: {str(e)}",
                "logs": {},
                "success": False,
                "error": str(e)
            }