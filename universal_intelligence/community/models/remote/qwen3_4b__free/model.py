from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "qwen/qwen3-4b:free"
    _description: ClassVar[str] = (
        "Qwen3-4B is a 4 billion parameter dense language model from the Qwen3 series, designed to support both general-purpose and reasoning-intensive tasks. It introduces a dual-mode architecture—thinking and non-thinking—allowing dynamic switching between high-precision logical reasoning and efficient dialogue generation. This makes it well-suited for multi-turn chat, instruction following, and complex agent workflows."
    )

    _inference_configuration: ClassVar[InferenceConfiguration] = {"openrouter": {"max_new_tokens": 2500, "temperature": 0.1}}

    def __init__(self, *args, **kwargs) -> None:
        """Initialize model with specified engine and configuration."""
        super().__init__(
            interface_config={
                "name": self._name,
                "inference_configuration": self._inference_configuration,
            },
            *args,
            **kwargs,
        )

    @classmethod
    def contract(cls) -> Contract:
        return generate_standard_contract(cls._name, cls._description)

    @classmethod
    def compatibility(cls) -> list[Compatibility]:
        return generate_standard_compatibility()
