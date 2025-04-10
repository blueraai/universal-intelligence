from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "qwen/qwen2.5-coder-7b-instruct"
    _description: ClassVar[str] = (
        "Qwen2.5-Coder-7B-Instruct is a 7B parameter instruction-tuned language model optimized for code-related tasks such as code generation, reasoning, and bug fixing. Based on the Qwen2.5 architecture, it incorporates enhancements like RoPE, SwiGLU, RMSNorm, and GQA attention with support for up to 128K tokens using YaRN-based extrapolation. It is trained on a large corpus of source code, synthetic data, and text-code grounding, providing robust performance across programming languages and agentic coding workflows. This model is part of the Qwen2.5-Coder family and offers strong compatibility with tools like vLLM for efficient deployment. Released under the Apache 2.0 license."
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
