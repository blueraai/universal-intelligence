from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "microsoft/mai-ds-r1:free"
    _description: ClassVar[str] = (
        "MAI-DS-R1 is a post-trained variant of DeepSeek-R1 developed by the Microsoft AI team to improve the model's responsiveness on previously blocked topics while enhancing its safety profile. Built on top of DeepSeek-R1's reasoning foundation, it integrates 110k examples from the Tulu-3 SFT dataset and 350k internally curated multilingual safety-alignment samples. The model retains strong reasoning, coding, and problem-solving capabilities, while unblocking a wide range of prompts previously restricted in R1. MAI-DS-R1 demonstrates improved performance on harm mitigation benchmarks and maintains competitive results across general reasoning tasks. It surpasses R1-1776 in satisfaction metrics for blocked queries and reduces leakage in harmful content categories. The model is based on a transformer MoE architecture and is suitable for general-purpose use cases, excluding high-stakes domains such as legal, medical, or autonomous systems."
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
