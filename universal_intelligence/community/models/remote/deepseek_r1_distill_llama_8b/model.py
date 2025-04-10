from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "deepseek/deepseek-r1-distill-llama-8b"
    _description: ClassVar[str] = (
        "DeepSeek R1 Distill Llama 8B is a distilled large language model based on [Llama-3.1-8B-Instruct](/meta-llama/llama-3.1-8b-instruct), using outputs from [DeepSeek R1](/deepseek/deepseek-r1). The model combines advanced distillation techniques to achieve high performance across multiple benchmarks, including:- AIME 2024 pass@1: 50.4- MATH-500 pass@1: 89.1- CodeForces Rating: 1205 The model leverages fine-tuning from DeepSeek R1's outputs, enabling competitive performance comparable to larger frontier models. Hugging Face: - [Llama-3.1-8B](https://huggingface.co/meta-llama/Llama-3.1-8B) - [DeepSeek-R1-Distill-Llama-8B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-8B)   |"
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
