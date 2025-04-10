from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "google/gemini-2.5-flash-preview:thinking"
    _description: ClassVar[str] = (
        "Gemini 2.5 Flash is Google's state-of-the-art workhorse model, specifically designed for advanced reasoning, coding, mathematics, and scientific tasks. It includes built-in 'thinking' capabilities, enabling it to provide responses with greater accuracy and nuanced context handling.  Note: This model is available in two variants: thinking and non-thinking. The output pricing varies significantly depending on whether the thinking capability is active. If you select the standard variant (without the ':thinking' suffix), the model will explicitly avoid generating thinking tokens.  To utilize the thinking capability and receive thinking tokens, you must choose the ':thinking' variant, which will then incur the higher thinking-output pricing.  Additionally, Gemini 2.5 Flash is configurable through the 'max tokens for reasoning' parameter, as described in the documentation (https://openrouter.ai/docs/use-cases/reasoning-tokens#max-tokens-for-reasoning)."
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
