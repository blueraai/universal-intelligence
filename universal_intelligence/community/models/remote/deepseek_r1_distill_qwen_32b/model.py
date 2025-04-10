from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "deepseek/deepseek-r1-distill-qwen-32b"
    _description: ClassVar[str] = (
        "DeepSeek R1 Distill Qwen 32B is a distilled large language model based on [Qwen 2.5 32B](https://huggingface.co/Qwen/Qwen2.5-32B), using outputs from [DeepSeek R1](/deepseek/deepseek-r1). It outperforms OpenAI's o1-mini across various benchmarks, achieving new state-of-the-art results for dense models. Other benchmark results include:- AIME 2024 pass@1: 72.6- MATH-500 pass@1: 94.3- CodeForces Rating: 1691 The model leverages fine-tuning from DeepSeek R1's outputs, enabling competitive performance comparable to larger frontier models."
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
