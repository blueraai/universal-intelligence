from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "x-ai/grok-3-mini-beta"
    _description: ClassVar[str] = (
        "Grok 3 Mini is a lightweight, smaller thinking model. Unlike traditional models that generate answers immediately, Grok 3 Mini thinks before responding. It's ideal for reasoning-heavy tasks that don't demand extensive domain knowledge, and shines in math-specific and quantitative use cases, such as solving challenging puzzles or math problems. Transparent 'thinking' traces accessible. Defaults to low reasoning, can boost with setting `reasoning: { effort: 'high' }` Note: That there are two xAI endpoints for this model. By default when using this model we will always route you to the base endpoint. If you want the fast endpoint you can add `provider: { sort: throughput}`, to sort by throughput instead. "
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
