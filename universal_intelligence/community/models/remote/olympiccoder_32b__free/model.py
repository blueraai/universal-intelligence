from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "open-r1/olympiccoder-32b:free"
    _description: ClassVar[str] = (
        "OlympicCoder-32B is a high-performing open-source model fine-tuned using the CodeForces-CoTs dataset, containing approximately 100,000 chain-of-thought programming samples. It excels at complex competitive programming benchmarks, such as IOI 2024 and Codeforces-style challenges, frequently surpassing state-of-the-art closed-source models. OlympicCoder-32B provides advanced reasoning, coherent multi-step problem-solving, and robust code generation capabilities, demonstrating significant potential for olympiad-level competitive programming applications."
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
