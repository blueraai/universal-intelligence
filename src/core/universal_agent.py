from abc import ABC, abstractmethod
from typing import Any

from src.core.universal_model import AbstractUniversalModel
from src.core.universal_tool import AbstractUniversalTool
from src.core.utils.types import Compatibility, Contract, Message, Requirement


class AbstractUniversalAgent(ABC):
    """Abstract base class for Universal Agents."""

    @classmethod
    @abstractmethod
    def contract(cls) -> Contract:
        """Get the contract for the agent."""
        pass

    @classmethod
    @abstractmethod
    def requirements(cls) -> list[Requirement]:
        """Get the requirements for the agent."""
        pass

    @classmethod
    @abstractmethod
    def compatibility(cls) -> list[Compatibility]:
        """Get the compatibility for the agent."""
        pass

    @abstractmethod
    def __init__(
        self,
        universal_model: AbstractUniversalModel | None = None,
        expand_tools: list[AbstractUniversalTool] | None = None,
        expand_team: list["AbstractUniversalAgent"] | None = None,
    ) -> None:
        """
        Initialize a Universal Agent.

        Args:
            universal_model: The model powering this agent
            expand_tools: List of tools to connect to the agent
            expand_team: List of other agents to connect to this agent
        """
        pass

    @abstractmethod
    def process(
        self,
        input: Any | list[Message] | None = None,
        context: list[Any] | None = None,
        configuration: dict | None = None,
        remember: bool = False,
        stream: bool = False,
        extra_tools: list[AbstractUniversalTool] | None = None,
        extra_team: list["AbstractUniversalAgent"] | None = None,
        keep_alive: bool = False,
    ) -> tuple[Any, dict]:
        """
        Process input through the agent.

        Args:
            input: Input or list of input dictionaries
            context: Optional list of context items (multimodal supported)
            configuration: Optional runtime configuration
            remember: Whether to remember this interaction in history
            stream: Whether to stream output asynchronously
            extra_tools: Additional tools for this specific inference
            extra_team: Additional agents for this specific inference
            keep_alive: Whether to keep the underlaying model loaded for faster consecutive interactions

        Returns:
            Tuple containing the agent output and processing logs
        """
        pass

    @abstractmethod
    def load(self) -> None:
        """Load agent's model into memory"""
        pass

    @abstractmethod
    def unload(self) -> None:
        """Unload agent's model from memory"""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Reset agent's chat history"""
        pass

    @abstractmethod
    def loaded(self) -> bool:
        """Check if agent's model is loaded"""
        pass

    @abstractmethod
    def connect(
        self,
        universal_tools: list[AbstractUniversalTool] | None = None,
        universal_agents: list["AbstractUniversalAgent"] | None = None,
    ) -> None:
        """
        Connect additional tools and agents.

        Args:
            universal_tools: List of tools to connect
            universal_agents: List of agents to connect
        """
        pass

    @abstractmethod
    def disconnect(
        self,
        universal_tools: list[AbstractUniversalTool] | None = None,
        universal_agents: list["AbstractUniversalAgent"] | None = None,
    ) -> None:
        """
        Disconnect tools and agents.

        Args:
            universal_tools: List of tools to disconnect
            universal_agents: List of agents to disconnect
        """
        pass
