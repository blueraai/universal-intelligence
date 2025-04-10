from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "nothingiisreal/mn-celeste-12b"
    _description: ClassVar[str] = (
        "A specialized story writing and roleplaying model based on Mistral's NeMo 12B Instruct. Fine-tuned on curated datasets including Reddit Writing Prompts and Opus Instruct 25K. This model excels at creative writing, offering improved NSFW capabilities, with smarter and more active narration. It demonstrates remarkable versatility in both SFW and NSFW scenarios, with strong Out of Character (OOC) steering capabilities, allowing fine-tuned control over narrative direction and character behavior. Check out the model's [HuggingFace page](https://huggingface.co/nothingiisreal/MN-12B-Celeste-V1.9) for details on what parameters and prompts work best!"
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
