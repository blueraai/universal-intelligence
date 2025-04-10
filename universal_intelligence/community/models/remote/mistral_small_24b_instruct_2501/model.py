from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "mistralai/mistral-small-24b-instruct-2501"
    _description: ClassVar[str] = (
        "Mistral Small 3 is a 24B-parameter language model optimized for low-latency performance across common AI tasks. Released under the Apache 2.0 license, it features both pre-trained and instruction-tuned versions designed for efficient local deployment. The model achieves 81% accuracy on the MMLU benchmark and performs competitively with larger models like Llama 3.3 70B and Qwen 32B, while operating at three times the speed on equivalent hardware. [Read the blog post about the model here.](https://mistral.ai/news/mistral-small-3/)"
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
