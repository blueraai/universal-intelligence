from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "google/gemma-3-1b-it:free"
    _description: ClassVar[str] = (
        "Gemma 3 1B is the smallest of the new Gemma 3 family. It handles context windows up to 32k tokens, understands over 140 languages, and offers improved math, reasoning, and chat capabilities, including structured outputs and function calling. Note: Gemma 3 1B is not multimodal. For the smallest multimodal Gemma 3 model, please see [Gemma 3 4B](google/gemma-3-4b-it)"
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
