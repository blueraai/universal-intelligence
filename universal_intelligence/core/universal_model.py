from abc import ABC, abstractmethod
from typing import Any

from .utils.types import Compatibility, Contract, Message, QuantizationSettings


class AbstractUniversalModel(ABC):
    """Abstract base class for Universal Models."""

    @classmethod
    @abstractmethod
    def contract(cls) -> Contract:
        """
        Get the contract for the model. Describes the model's description, interface, and capabilities.
        """
        pass

    @classmethod
    @abstractmethod
    def compatibility(cls) -> list[Compatibility]:
        """
        Get the compatibility for the model.
        """
        pass

    @abstractmethod
    def __init__(
        self,
        engine: str | list[str] | None = None,
        quantization: str | list[str] | QuantizationSettings | None = None,
        max_memory_allocation: float | None = None,
        configuration: dict | None = None,
    ) -> None:
        """
        Initialize a Universal Model.

        Args:
            engine: Optional engine specification (e.g., 'transformers', 'llama.cpp', -or- ordered by priority ['transformers', 'llama.cpp'])
            quantization: Optional quantization specification (e.g., 'Q4_K_M', 'Q8_0' -or- ['Q4_K_M', 'Q8_0'] -or- {'default': 'Q4_K_M', 'min_precision': '4bit', 'max_precision': '8bit'})
            max_memory_allocation: Optional maximum memory allocation in percentage
            configuration: Optional configuration dictionary for model and processor settings
        """
        pass

    @abstractmethod
    def process(self, input: Any | list[Message] | None = None, context: list[Any] | None = None, configuration: dict | None = None, remember: bool = False, keep_alive: bool = False) -> tuple[Any, dict]:
        """
        Process input through the model.

        Args:
            input: Input to process
            context: Optional context for the model
            configuration: Optional configuration for processing
            remember: Whether to remember the interaction in history
            keep_alive: Whether to keep the model loaded for faster consecutive interactions

        Returns:
            Tuple of (output, metadata)
        """
        pass

    @abstractmethod
    def load(self) -> None:
        """Load model into memory"""
        pass

    @abstractmethod
    def unload(self) -> None:
        """Unload model from memory"""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Reset model chat history"""
        pass

    @abstractmethod
    def loaded(self) -> bool:
        """Check if model is loaded"""
        pass

    @abstractmethod
    def configuration(self) -> dict:
        """Get model configuration"""
        pass
