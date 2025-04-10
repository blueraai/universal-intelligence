from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "thudm/glm-z1-9b:free"
    _description: ClassVar[str] = (
        "GLM-Z1-9B-0414 is a 9B-parameter language model developed by THUDM as part of the GLM-4 family. It incorporates techniques originally applied to larger GLM-Z1 models, including extended reinforcement learning, pairwise ranking alignment, and training on reasoning-intensive tasks such as mathematics, code, and logic. Despite its smaller size, it demonstrates strong performance on general-purpose reasoning tasks and outperforms many open-source models in its weight class."
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
