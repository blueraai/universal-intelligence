from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "arcee-ai/arcee-blitz"
    _description: ClassVar[str] = (
        "Arcee Blitz is a 24 B‑parameter dense model distilled from DeepSeek and built on Mistral architecture for 'everyday' chat. The distillation‑plus‑refinement pipeline trims compute while keeping DeepSeek‑style reasoning, so Blitz punches above its weight on MMLU, GSM‑8K and BBH compared with other mid‑size open models. With a default 128 k context window and competitive throughput, it serves as a cost‑efficient workhorse for summarization, brainstorming and light code help. Internally, Arcee uses Blitz as the default writer in Conductor pipelines when the heavier Virtuoso line is not required. Users therefore get near‑70 B quality at ~⅓ the latency and price. "
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
