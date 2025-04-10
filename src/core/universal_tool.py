from abc import ABC, abstractmethod

from src.core.utils.types import Contract, Requirement


class AbstractUniversalTool(ABC):
    """Abstract base class for Universal Tools."""

    @classmethod
    @abstractmethod
    def contract(cls) -> Contract:
        """Get the contract for the tool."""
        pass

    @classmethod
    @abstractmethod
    def requirements(cls) -> list[Requirement]:
        """Get the requirements for the tool."""
        pass

    @abstractmethod
    def __init__(self, configuration: dict | None = None) -> None:
        """
        Initialize a Universal Tool.

        Args:
            configuration: Tool configuration including required credentials
        """
        pass

    # Note: Additional methods are defined by the specific tool implementation
    # and documented in the tool's contract
