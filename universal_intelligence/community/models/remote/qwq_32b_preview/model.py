from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "qwen/qwq-32b-preview"
    _description: ClassVar[str] = (
        "QwQ-32B-Preview is an experimental research model focused on AI reasoning capabilities developed by the Qwen Team. As a preview release, it demonstrates promising analytical abilities while having several important limitations: 1. **Language Mixing and Code-Switching**: The model may mix languages or switch between them unexpectedly, affecting response clarity. 2. **Recursive Reasoning Loops**: The model may enter circular reasoning patterns, leading to lengthy responses without a conclusive answer. 3. **Safety and Ethical Considerations**: The model requires enhanced safety measures to ensure reliable and secure performance, and users should exercise caution when deploying it. 4. **Performance and Benchmark Limitations**: The model excels in math and coding but has room for improvement in other areas, such as common sense reasoning and nuanced language understanding."
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
