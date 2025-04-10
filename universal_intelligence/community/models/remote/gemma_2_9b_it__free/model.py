from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "google/gemma-2-9b-it:free"
    _description: ClassVar[str] = (
        "Gemma 2 9B by Google is an advanced, open-source language model that sets a new standard for efficiency and performance in its size class. Designed for a wide variety of tasks, it empowers developers and researchers to build innovative applications, while maintaining accessibility, safety, and cost-effectiveness. See the [launch announcement](https://blog.google/technology/developers/google-gemma-2/) for more details. Usage of Gemma is subject to Google's [Gemma Terms of Use](https://ai.google.dev/gemma/terms)."
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
