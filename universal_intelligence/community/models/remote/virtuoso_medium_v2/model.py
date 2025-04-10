from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "arcee-ai/virtuoso-medium-v2"
    _description: ClassVar[str] = (
        "Virtuoso‑Medium‑v2 is a 32 B model distilled from DeepSeek‑v3 logits and merged back onto a Qwen 2.5 backbone, yielding a sharper, more factual successor to the original Virtuoso Medium. The team harvested ~1.1 B logit tokens and applied 'fusion‑merging' plus DPO alignment, which pushed scores past Arcee‑Nova 2024 and many 40 B‑plus peers on MMLU‑Pro, MATH and HumanEval. With a 128 k context and aggressive quantization options (from BF16 down to 4‑bit GGUF), it balances capability with deployability on single‑GPU nodes. Typical use cases include enterprise chat assistants, technical writing aids and medium‑complexity code drafting where Virtuoso‑Large would be overkill. "
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
