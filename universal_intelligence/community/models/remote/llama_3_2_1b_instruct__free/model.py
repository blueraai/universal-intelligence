from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "meta-llama/llama-3.2-1b-instruct:free"
    _description: ClassVar[str] = (
        "Llama 3.2 1B is a 1-billion-parameter language model focused on efficiently performing natural language tasks, such as summarization, dialogue, and multilingual text analysis. Its smaller size allows it to operate efficiently in low-resource environments while maintaining strong task performance. Supporting eight core languages and fine-tunable for more, Llama 1.3B is ideal for businesses or developers seeking lightweight yet powerful AI solutions that can operate in diverse multilingual settings without the high computational demand of larger models. Click here for the [original model card](https://github.com/meta-llama/llama-models/blob/main/models/llama3_2/MODEL_CARD.md). Usage of this model is subject to [Meta's Acceptable Use Policy](https://www.llama.com/llama3/use-policy/)."
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
