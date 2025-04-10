from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "cognitivecomputations/dolphin3.0-r1-mistral-24b:free"
    _description: ClassVar[str] = (
        "Dolphin 3.0 R1 is the next generation of the Dolphin series of instruct-tuned models.  Designed to be the ultimate general purpose local model, enabling coding, math, agentic, function calling, and general use cases. The R1 version has been trained for 3 epochs to reason using 800k reasoning traces from the Dolphin-R1 dataset. Dolphin aims to be a general purpose reasoning instruct model, similar to the models behind ChatGPT, Claude, Gemini. Part of the [Dolphin 3.0 Collection](https://huggingface.co/collections/cognitivecomputations/dolphin-30-677ab47f73d7ff66743979a3) Curated and trained by [Eric Hartford](https://huggingface.co/ehartford), [Ben Gitter](https://huggingface.co/bigstorm), [BlouseJury](https://huggingface.co/BlouseJury) and [Cognitive Computations](https://huggingface.co/cognitivecomputations)"
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
