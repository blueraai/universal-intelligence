from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "moonshotai/moonlight-16b-a3b-instruct:free"
    _description: ClassVar[str] = (
        "Moonlight-16B-A3B-Instruct is a 16B-parameter Mixture-of-Experts (MoE) language model developed by Moonshot AI. It is optimized for instruction-following tasks with 3B activated parameters per inference. The model advances the Pareto frontier in performance per FLOP across English, coding, math, and Chinese benchmarks. It outperforms comparable models like Llama3-3B and Deepseek-v2-Lite while maintaining efficient deployment capabilities through Hugging Face integration and compatibility with popular inference engines like vLLM12."
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
