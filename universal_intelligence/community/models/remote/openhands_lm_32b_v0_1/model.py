from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "all-hands/openhands-lm-32b-v0.1"
    _description: ClassVar[str] = (
        "OpenHands LM v0.1 is a 32B open-source coding model fine-tuned from Qwen2.5-Coder-32B-Instruct using reinforcement learning techniques outlined in SWE-Gym. It is optimized for autonomous software development agents and achieves strong performance on SWE-Bench Verified, with a 37.2% resolve rate. The model supports a 128K token context window, making it well-suited for long-horizon code reasoning and large codebase tasks. OpenHands LM is designed for local deployment and runs on consumer-grade GPUs such as a single 3090. It enables fully offline agent workflows without dependency on proprietary APIs. This release is intended as a research preview, and future updates aim to improve generalizability, reduce repetition, and offer smaller variants."
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
