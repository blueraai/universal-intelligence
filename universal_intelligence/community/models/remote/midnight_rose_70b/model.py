from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "sophosympatheia/midnight-rose-70b"
    _description: ClassVar[str] = (
        "A merge with a complex family tree, this model was crafted for roleplaying and storytelling. Midnight Rose is a successor to Rogue Rose and Aurora Nights and improves upon them both. It wants to produce lengthy output by default and is the best creative writing merge produced so far by sophosympatheia. Descending from earlier versions of Midnight Rose and [Wizard Tulu Dolphin 70B](https://huggingface.co/sophosympatheia/Wizard-Tulu-Dolphin-70B-v1.0), it inherits the best qualities of each."
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
