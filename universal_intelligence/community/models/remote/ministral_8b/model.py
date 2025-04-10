from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "mistral/ministral-8b"
    _description: ClassVar[str] = (
        "Ministral 8B is a state-of-the-art language model optimized for on-device and edge computing. Designed for efficiency in knowledge-intensive tasks, commonsense reasoning, and function-calling, it features a specialized interleaved sliding-window attention mechanism, enabling faster and more memory-efficient inference. Ministral 8B excels in local, low-latency applications such as offline translation, smart assistants, autonomous robotics, and local analytics. The model supports up to 128k context length and can function as a performant intermediary in multi-step agentic workflows, efficiently handling tasks like input parsing, API calls, and task routing. It consistently outperforms comparable models like Mistral 7B across benchmarks, making it particularly suitable for compute-efficient, privacy-focused scenarios."
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
