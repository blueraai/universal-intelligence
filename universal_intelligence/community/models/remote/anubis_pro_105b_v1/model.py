from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "thedrummer/anubis-pro-105b-v1"
    _description: ClassVar[str] = (
        "Anubis Pro 105B v1 is an expanded and refined variant of Meta's Llama 3.3 70B, featuring 50% additional layers and further fine-tuning to leverage its increased capacity. Designed for advanced narrative, roleplay, and instructional tasks, it demonstrates enhanced emotional intelligence, creativity, nuanced character portrayal, and superior prompt adherence compared to smaller models. Its larger parameter count allows for deeper contextual understanding and extended reasoning capabilities, optimized for engaging, intelligent, and coherent interactions."
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
