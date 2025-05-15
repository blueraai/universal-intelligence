from typing import Any, ClassVar, Optional, Union, List, Dict, Tuple

from ....community.__utils__.logger import Color, Logger, LogLevel
from ....community.models.default import UniversalModel
from ....core.universal_agent import AbstractUniversalAgent
from ....core.universal_model import AbstractUniversalModel
from ....core.universal_tool import AbstractUniversalTool
from ....core.utils.types import Compatibility, Contract, Message, Requirement

from .flow import Flow
from .nodes import Node


class FlowUniversalAgent(AbstractUniversalAgent):
    """A Universal Agent implementation that supports PocketFlow-like workflow execution.
    
    This agent extends the Universal Agent interface with flow-based execution capabilities,
    allowing complex AI workflows to be created through connected processing nodes.
    """

    _contract: ClassVar[Contract] = {
        "name": "Flow-based Agent",
        "description": "A Universal Agent that supports PocketFlow-like workflow execution",
        "methods": [
            {
                "name": "create_flow",
                "description": "Create a new flow with connected nodes",
                "arguments": [
                    {
                        "name": "start",
                        "type": "Node",
                        "schema": {},
                        "description": "The starting node for the flow",
                        "required": True,
                    },
                    {
                        "name": "connections",
                        "type": "Dict",
                        "schema": {},
                        "description": "Dictionary mapping nodes to their connections",
                        "required": False,
                    },
                ],
                "outputs": [
                    {
                        "type": "Flow",
                        "schema": {},
                        "description": "The created flow",
                        "required": True,
                    }
                ],
            },
            {
                "name": "process",
                "description": "Process input through the agent, optionally using a flow",
                "arguments": [
                    {
                        "name": "input",
                        "type": "str | List[Message]",
                        "schema": {
                            "nested": [
                                {
                                    "name": "role",
                                    "type": "str",
                                    "schema": {"pattern": "^(system|user|assistant)$"},
                                    "description": "The role of the message sender",
                                    "required": True,
                                },
                                {
                                    "name": "content",
                                    "type": "str",
                                    "schema": {},
                                    "description": "The content of the message",
                                    "required": True,
                                },
                            ]
                        },
                        "description": "Input string or list of messages in chat format",
                        "required": True,
                    },
                    {
                        "name": "context",
                        "type": "List[Any]",
                        "schema": {},
                        "description": "Optional context items to prepend as system messages",
                        "required": False,
                    },
                    {
                        "name": "configuration",
                        "type": "Dict",
                        "schema": {},
                        "description": "Optional runtime configuration",
                        "required": False,
                    },
                    {
                        "name": "flow",
                        "type": "Flow",
                        "schema": {},
                        "description": "Flow to execute",
                        "required": False,
                    },
                    {
                        "name": "shared_state",
                        "type": "Dict",
                        "schema": {},
                        "description": "Initial shared state for flow execution",
                        "required": False,
                    },
                    {
                        "name": "remember",
                        "type": "bool",
                        "schema": {},
                        "description": "Whether to remember this interaction in history",
                        "required": False,
                    },
                    {
                        "name": "stream",
                        "type": "bool",
                        "schema": {},
                        "description": "Whether to stream output asynchronously",
                        "required": False,
                    },
                    {
                        "name": "extra_tools",
                        "type": "List[AbstractUniversalTool]",
                        "schema": {},
                        "description": "Additional tools for this specific inference",
                        "required": False,
                    },
                    {
                        "name": "extra_team",
                        "type": "List[AbstractUniversalAgent]",
                        "schema": {},
                        "description": "Additional agents for this specific inference",
                        "required": False,
                    },
                    {
                        "name": "keep_alive",
                        "type": "bool",
                        "schema": {},
                        "description": "Keep underlaying model loaded for faster consecutive interactions",
                        "required": False,
                    },
                ],
                "outputs": [
                    {
                        "type": "Tuple[Any, Dict]",
                        "schema": {
                            "nested": [
                                {
                                    "name": "response",
                                    "type": "str",
                                    "schema": {},
                                    "description": "Generated text response",
                                    "required": True,
                                },
                                {
                                    "name": "logs",
                                    "type": "Dict",
                                    "schema": {},
                                    "description": "Processing logs and metadata",
                                    "required": True,
                                },
                            ]
                        },
                        "description": "Generated response and processing logs",
                        "required": True,
                    }
                ],
            },
            # Additional standard Universal Agent methods
            {
                "name": "load",
                "description": "Load the agent's model into memory",
                "arguments": [],
                "outputs": [
                    {
                        "type": "None",
                        "schema": {},
                        "description": "No return value",
                        "required": True,
                    }
                ],
            },
            {
                "name": "loaded",
                "description": "Check if the agent's model is loaded",
                "arguments": [],
                "outputs": [
                    {
                        "type": "bool",
                        "schema": {},
                        "description": "True if the model is loaded, False otherwise",
                        "required": True,
                    }
                ],
            },
            {
                "name": "unload",
                "description": "Unload the agent's model from memory",
                "arguments": [],
                "outputs": [
                    {
                        "type": "None",
                        "schema": {},
                        "description": "No return value",
                        "required": True,
                    }
                ],
            },
            {
                "name": "reset",
                "description": "Reset the agent's chat history",
                "arguments": [],
                "outputs": [
                    {
                        "type": "None",
                        "schema": {},
                        "description": "No return value",
                        "required": True,
                    }
                ],
            },
            {
                "name": "connect",
                "description": "Connect additional tools and agents",
                "arguments": [
                    {
                        "name": "tools",
                        "type": "List[AbstractUniversalTool]",
                        "schema": {},
                        "description": "Additional tools to connect",
                        "required": False,
                    },
                    {
                        "name": "agents",
                        "type": "List[AbstractUniversalAgent]",
                        "schema": {},
                        "description": "Additional agents to connect",
                        "required": False,
                    },
                ],
                "outputs": [
                    {
                        "type": "None",
                        "schema": {},
                        "description": "No return value",
                        "required": True,
                    }
                ],
            },
            {
                "name": "disconnect",
                "description": "Disconnect tools and agents",
                "arguments": [
                    {
                        "name": "tools",
                        "type": "List[AbstractUniversalTool]",
                        "schema": {},
                        "description": "Tools to disconnect",
                        "required": False,
                    },
                    {
                        "name": "agents",
                        "type": "List[AbstractUniversalAgent]",
                        "schema": {},
                        "description": "Agents to disconnect",
                        "required": False,
                    },
                ],
                "outputs": [
                    {
                        "type": "None",
                        "schema": {},
                        "description": "No return value",
                        "required": True,
                    }
                ],
            },
        ],
    }

    _requirements: ClassVar[list[Requirement]] = []

    _compatibility: ClassVar[list[Compatibility]] = [
        {
            "engine": "any",
            "quantization": "any",
            "devices": ["cuda", "mps", "cpu"],
            "memory": 0.0,
            "dependencies": ["pyyaml"],
            "precision": 4,
        }
    ]

    _default_tools: ClassVar[list[AbstractUniversalTool]] = []
    _default_team: ClassVar[list[AbstractUniversalAgent]] = []

    @classmethod
    def contract(cls) -> Contract:
        return cls._contract.copy()

    @classmethod
    def compatibility(cls) -> list[Compatibility]:
        return cls._compatibility.copy()

    @classmethod
    def requirements(cls) -> list[Requirement]:
        return cls._requirements.copy()

    def __init__(
        self,
        model: Optional[AbstractUniversalModel] = None,
        expand_tools: Optional[list[AbstractUniversalTool]] = None,
        expand_team: Optional[list["AbstractUniversalAgent"]] = None,
        verbose: Union[bool, str] = "DEFAULT",
        configuration: Optional[dict] = None,
    ) -> None:
        """Initialize a Flow-based Universal Agent.
        
        Args:
            model: The model powering this agent
            expand_tools: List of tools to connect to the agent
            expand_team: List of other agents to connect to this agent
            verbose: Verbosity level for logging
            configuration: Optional configuration dictionary for the agent
        """
        self._log_level = LogLevel.NONE
        if verbose:
            if isinstance(verbose, bool):
                self._log_level = LogLevel.DEFAULT if verbose else LogLevel.NONE
            elif isinstance(verbose, str) and verbose.upper() in LogLevel.__members__:
                self._log_level = LogLevel[verbose.upper()]
            else:
                raise ValueError(f"Invalid verbose value: {verbose} (must be bool or str)")

        with Logger(self._log_level) as logger:
            logger.print(message=f'* Initializing agent.. ({self._contract["name"]}) *\n', color=Color.WHITE)

            logger.print(prefix="Agent", message="Setting model..", color=Color.GRAY)
            self.model = model if model is not None else UniversalModel(verbose=verbose if self._log_level == LogLevel.DEBUG else "NONE")
            logger.print(prefix="Agent", message="Setting tools..", color=Color.GRAY)
            self.tools = self._default_tools + (expand_tools if expand_tools else [])
            logger.print(prefix="Agent", message="Setting team..", color=Color.GRAY)
            self.team = self._default_team + (expand_team if expand_team else [])
            logger.print(prefix="Agent", message="Configuring..", color=Color.GRAY)
            self._configuration = configuration if configuration else {}
            logger.print(prefix="Agent", message="Initialization complete\n", color=Color.GREEN)

    def create_flow(self, start: Node, connections: Optional[Dict[Node, Dict[str, Node]]] = None) -> Flow:
        """Create a new flow with connected nodes.
        
        Args:
            start: The starting node for the flow
            connections: Dictionary mapping nodes to their connections
            
        Returns:
            The created flow
        """
        # Implementation to be completed
        flow = Flow(start=start)
        
        # Apply connections if provided
        if connections:
            for node, node_connections in connections.items():
                for action, target in node_connections.items():
                    node.connections[action] = target
                    
        return flow

    def process(
        self,
        input: Union[str, list[Message]],
        context: Optional[list[Any]] = None,
        configuration: Optional[dict] = None,
        flow: Optional[Flow] = None,
        shared_state: Optional[dict] = None,
        remember: bool = False,
        stream: bool = False,
        extra_tools: Optional[list[AbstractUniversalTool]] = None,
        extra_team: Optional[list["AbstractUniversalAgent"]] = None,
        keep_alive: bool = False,
    ) -> Tuple[Any, dict]:
        """Process input through the agent, optionally using a flow.
        
        Args:
            input: Input string or list of messages in chat format
            context: Optional context items to prepend as system messages
            configuration: Optional runtime configuration
            flow: Flow to execute
            shared_state: Initial shared state for flow execution
            remember: Whether to remember this interaction in history
            stream: Whether to stream output asynchronously
            extra_tools: Additional tools for this specific inference
            extra_team: Additional agents for this specific inference
            keep_alive: Keep underlaying model loaded for faster consecutive interactions
            
        Returns:
            Tuple containing the generated response and processing logs
        """
        with Logger(self._log_level) as logger:
            logger.print(message=f'* Invoking agent.. ({self._contract["name"]}) *\n', color=Color.WHITE)
            
            # Handle flow-based execution if a flow is provided
            if flow:
                logger.print(prefix="Agent", message="Executing flow..", color=Color.CYAN)
                
                # Initialize shared state
                state = shared_state.copy() if shared_state else {}
                
                # Add input to shared state
                if isinstance(input, str):
                    state["input"] = input
                else:
                    state["messages"] = input
                    state["input"] = input[-1]["content"] if input else ""
                
                # Add tools and team to shared state
                state["tools"] = self.tools + (extra_tools if extra_tools else [])
                state["team"] = self.team + (extra_team if extra_team else [])
                state["model"] = self.model
                state["configuration"] = configuration
                
                # Execute the flow
                final_state = flow.run(state)
                
                # Get result from shared state
                result = final_state.get("result", "No result produced by flow")
                
                logger.print(prefix="Agent", message="Flow execution complete", color=Color.GREEN)
                
                return result, {
                    "flow_execution": True,
                    "final_state": final_state,
                    "stream": stream,
                }
            
            # If no flow is provided, fall back to standard processing
            # For initial implementation, we'll use a simplified version
            
            # Convert input to string if it's a message list
            query = input if isinstance(input, str) else input[-1]["content"]
            
            logger.print(prefix="Agent", message="Generating output..", color=Color.CYAN)
            
            # Process with model
            response, logs = self.model.process(
                query,
                context=context,
                configuration=configuration,
                remember=remember,
                keep_alive=keep_alive,
            )
            
            logger.print(prefix="Agent", message="Output generated\n", color=Color.GREEN)
            
            return response, {
                "model_logs": logs,
                "stream": stream,
            }

    def load(self) -> None:
        """Load the agent's model into memory."""
        with Logger(self._log_level) as logger:
            logger.print(message=f'* Loading agent.. ({self._contract["name"]}) *\n', color=Color.WHITE)
            logger.print(prefix="Agent", message="Loading model..", color=Color.CYAN)
            self.model.load()
            logger.print(prefix="Agent", message="Loading model..", color=Color.GRAY, replace_last_line=True)
            logger.print(prefix="Agent", message="Model loaded\n", color=Color.GREEN)

    def loaded(self) -> bool:
        """Check if the agent's model is loaded"""
        with Logger(self._log_level):
            return self.model.loaded()

    def unload(self) -> None:
        """Unload the agent's model from memory."""
        with Logger(self._log_level) as logger:
            logger.print(message=f'* Unloading agent.. ({self._contract["name"]}) *\n', color=Color.WHITE)
            logger.print(prefix="Agent", message="Unloading model..", color=Color.CYAN)
            self.model.unload()
            logger.print(prefix="Agent", message="Unloading model..", color=Color.GRAY, replace_last_line=True)
            logger.print(prefix="Agent", message="Model unloaded\n", color=Color.GREEN)

    def reset(self) -> None:
        """Reset the agent's chat history."""
        with Logger(self._log_level) as logger:
            logger.print(message=f'* Resetting agent history.. ({self._contract["name"]}) *\n', color=Color.WHITE)
            logger.print(prefix="Agent", message="Resetting history..", color=Color.GRAY)
            self.model.reset()
            logger.print(prefix="Agent", message="History reset\n", color=Color.GREEN)

    def connect(
        self,
        tools: Optional[list[AbstractUniversalTool]] = None,
        agents: Optional[list["AbstractUniversalAgent"]] = None,
    ) -> None:
        """Connect additional tools and agents."""
        with Logger(self._log_level) as logger:
            logger.print(message=f'* Connecting additional tools and agents.. ({self._contract["name"]}) *\n', color=Color.WHITE)
            if tools:
                logger.print(prefix="Agent", message="Connecting tools..", color=Color.GRAY)
                self.tools.extend(tools)
            if agents:
                logger.print(prefix="Agent", message="Connecting agents..", color=Color.GRAY)
                self.team.extend(agents)
            logger.print(prefix="Agent", message="Tools and agents connected\n", color=Color.GREEN)

    def disconnect(
        self,
        tools: Optional[list[AbstractUniversalTool]] = None,
        agents: Optional[list["AbstractUniversalAgent"]] = None,
    ) -> None:
        """Disconnect tools and agents."""
        with Logger(self._log_level) as logger:
            logger.print(message=f'* Disconnecting additional tools and agents.. ({self._contract["name"]}) *\n', color=Color.WHITE)
            if tools:
                logger.print(prefix="Agent", message="Disconnecting tools..", color=Color.GRAY)
                self.tools = [t for t in self.tools if t not in tools]
            if agents:
                logger.print(prefix="Agent", message="Disconnecting agents..", color=Color.GRAY)
                self.team = [a for a in self.team if a not in agents]
            logger.print(prefix="Agent", message="Tools and agents disconnected\n", color=Color.GREEN)