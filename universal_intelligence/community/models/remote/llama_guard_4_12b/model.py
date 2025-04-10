from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "meta-llama/llama-guard-4-12b"
    _description: ClassVar[str] = (
        "Llama Guard 4 is a Llama 4 Scout-derived multimodal pretrained model, fine-tuned for content safety classification. Similar to previous versions, it can be used to classify content in both LLM inputs (prompt classification) and in LLM responses (response classification). It acts as an LLM—generating text in its output that indicates whether a given prompt or response is safe or unsafe, and if unsafe, it also lists the content categories violated. Llama Guard 4 was aligned to safeguard against the standardized MLCommons hazards taxonomy and designed to support multimodal Llama 4 capabilities. Specifically, it combines features from previous Llama Guard models, providing content moderation for English and multiple supported languages, along with enhanced capabilities to handle mixed text-and-image prompts, including multiple images. Additionally, Llama Guard 4 is integrated into the Llama Moderations API, extending robust safety classification to text and images."
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
