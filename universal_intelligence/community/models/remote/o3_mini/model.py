from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "openai/o3-mini"
    _description: ClassVar[str] = (
        "OpenAI o3-mini is a cost-efficient language model optimized for STEM reasoning tasks, particularly excelling in science, mathematics, and coding. This model supports the `reasoning_effort` parameter, which can be set to 'high', 'medium', or 'low' to control the thinking time of the model. The default is 'medium'. OpenRouter also offers the model slug `openai/o3-mini-high` to default the parameter to 'high'. The model features three adjustable reasoning effort levels and supports key developer capabilities including function calling, structured outputs, and streaming, though it does not include vision processing capabilities. The model demonstrates significant improvements over its predecessor, with expert testers preferring its responses 56% of the time and noting a 39% reduction in major errors on complex questions. With medium reasoning effort settings, o3-mini matches the performance of the larger o1 model on challenging reasoning evaluations like AIME and GPQA, while maintaining lower latency and cost."
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
