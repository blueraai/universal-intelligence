from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "undi95/toppy-m-7b"
    _description: ClassVar[str] = (
        "A wild 7B parameter model that merges several models using the new task_arithmetic merge method from mergekit. List of merged models:- NousResearch/Nous-Capybara-7B-V1.9- [HuggingFaceH4/zephyr-7b-beta](/models/huggingfaceh4/zephyr-7b-beta)- lemonilia/AshhLimaRP-Mistral-7B- Vulkane/120-Days-of-Sodom-LoRA-Mistral-7b- Undi95/Mistral-pippa-sharegpt-7b-qlora#merge #uncensored"
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
