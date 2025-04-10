from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "qwen/qwen3-30b-a3b"
    _description: ClassVar[str] = (
        "Qwen3, the latest generation in the Qwen large language model series, features both dense and mixture-of-experts (MoE) architectures to excel in reasoning, multilingual support, and advanced agent tasks. Its unique ability to switch seamlessly between a thinking mode for complex reasoning and a non-thinking mode for efficient dialogue ensures versatile, high-quality performance. Significantly outperforming prior models like QwQ and Qwen2.5, Qwen3 delivers superior mathematics, coding, commonsense reasoning, creative writing, and interactive dialogue capabilities. The Qwen3-30B-A3B variant includes 30.5 billion parameters (3.3 billion activated), 48 layers, 128 experts (8 activated per task), and supports up to 131K token contexts with YaRN, setting a new standard among open-source models."
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
