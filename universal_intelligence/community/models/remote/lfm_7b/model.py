from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "liquid/lfm-7b"
    _description: ClassVar[str] = (
        "LFM-7B, a new best-in-class language model. LFM-7B is designed for exceptional chat capabilities, including languages like Arabic and Japanese. Powered by the Liquid Foundation Model (LFM) architecture, it exhibits unique features like low memory footprint and fast inference speed.  LFM-7B is the world's best-in-class multilingual language model in English, Arabic, and Japanese. See the [launch announcement](https://www.liquid.ai/lfm-7b) for benchmarks and more info."
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
