from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "microsoft/phi-4-reasoning:free"
    _description: ClassVar[str] = (
        "Phi-4-reasoning is a 14B parameter dense decoder-only transformer developed by Microsoft, fine-tuned from Phi-4 to enhance complex reasoning capabilities. It uses a combination of supervised fine-tuning on chain-of-thought traces and reinforcement learning, targeting math, science, and code reasoning tasks. With a 32k context window and high inference efficiency, it is optimized for structured responses in a two-part format: reasoning trace followed by a final solution. The model achieves strong results on specialized benchmarks such as AIME, OmniMath, and LiveCodeBench, outperforming many larger models in structured reasoning tasks. It is released under the MIT license and intended for use in latency-constrained, English-only environments requiring reliable step-by-step logic. Recommended usage includes ChatML prompts and structured reasoning format for best results."
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
