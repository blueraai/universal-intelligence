from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "scb10x/llama3.1-typhoon2-8b-instruct"
    _description: ClassVar[str] = (
        "Llama3.1-Typhoon2-8B-Instruct is a Thai-English instruction-tuned model with 8 billion parameters, built on Llama 3.1. It significantly improves over its base model in Thai reasoning, instruction-following, and function-calling tasks, while maintaining competitive English performance. The model is optimized for bilingual interaction and performs well on Thai-English code-switching, MT-Bench, IFEval, and tool-use benchmarks. Despite its smaller size, it demonstrates strong generalization across math, coding, and multilingual benchmarks, outperforming comparable 8B models across most Thai-specific tasks. Full benchmark results and methodology are available in the [technical report.](https://arxiv.org/abs/2412.13702)"
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
