from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "eva-unit-01/eva-llama-3.33-70b"
    _description: ClassVar[str] = (
        "EVA Llama 3.33 70b is a roleplay and storywriting specialist model. It is a full-parameter finetune of [Llama-3.3-70B-Instruct](https://openrouter.ai/meta-llama/llama-3.3-70b-instruct) on mixture of synthetic and natural data. It uses Celeste 70B 0.1 data mixture, greatly expanding it to improve versatility, creativity and 'flavor' of the resulting model This model was built with Llama by Meta."
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
