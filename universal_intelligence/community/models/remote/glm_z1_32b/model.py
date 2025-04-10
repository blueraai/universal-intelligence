from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "thudm/glm-z1-32b"
    _description: ClassVar[str] = (
        "GLM-Z1-32B-0414 is an enhanced reasoning variant of GLM-4-32B, built for deep mathematical, logical, and code-oriented problem solving. It applies extended reinforcement learning—both task-specific and general pairwise preference-based—to improve performance on complex multi-step tasks. Compared to the base GLM-4-32B model, Z1 significantly boosts capabilities in structured reasoning and formal domains. The model supports enforced 'thinking' steps via prompt engineering and offers improved coherence for long-form outputs. It's optimized for use in agentic workflows, and includes support for long context (via YaRN), JSON tool calling, and fine-grained sampling configuration for stable inference. Ideal for use cases requiring deliberate, multi-step reasoning or formal derivations."
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
