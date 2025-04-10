from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "arcee-ai/caller-large"
    _description: ClassVar[str] = (
        "Caller Large is Arcee's specialist 'function‑calling' SLM built to orchestrate external tools and APIs. Instead of maximizing next‑token accuracy, training focuses on structured JSON outputs, parameter extraction and multi‑step tool chains, making Caller a natural choice for retrieval‑augmented generation, robotic process automation or data‑pull chatbots. It incorporates a routing head that decides when (and how) to invoke a tool versus answering directly, reducing hallucinated calls. The model is already the backbone of Arcee Conductor's auto‑tool mode, where it parses user intent, emits clean function signatures and hands control back once the tool response is ready. Developers thus gain an OpenAI‑style function‑calling UX without handing requests to a frontier‑scale model. "
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
