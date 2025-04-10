from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "openrouter/auto"
    _description: ClassVar[str] = (
        "Your prompt will be processed by a meta-model and routed to one of dozens of models (see below), optimizing for the best possible output. To see which model was used, visit [Activity](/activity), or read the `model` attribute of the response. Your response will be priced at the same rate as the routed model. The meta-model is powered by [Not Diamond](https://docs.notdiamond.ai/docs/how-not-diamond-works). Learn more in our [docs](/docs/model-routing). Requests will be routed to the following models:- [openai/gpt-4o-2024-08-06](/openai/gpt-4o-2024-08-06)- [openai/gpt-4o-2024-05-13](/openai/gpt-4o-2024-05-13)- [openai/gpt-4o-mini-2024-07-18](/openai/gpt-4o-mini-2024-07-18)- [openai/chatgpt-4o-latest](/openai/chatgpt-4o-latest)- [openai/o1-preview-2024-09-12](/openai/o1-preview-2024-09-12)- [openai/o1-mini-2024-09-12](/openai/o1-mini-2024-09-12)- [anthropic/claude-3.5-sonnet](/anthropic/claude-3.5-sonnet)- [anthropic/claude-3.5-haiku](/anthropic/claude-3.5-haiku)- [anthropic/claude-3-opus](/anthropic/claude-3-opus)- [anthropic/claude-2.1](/anthropic/claude-2.1)- [google/gemini-pro-1.5](/google/gemini-pro-1.5)- [google/gemini-flash-1.5](/google/gemini-flash-1.5)- [mistralai/mistral-large-2407](/mistralai/mistral-large-2407)- [mistralai/mistral-nemo](/mistralai/mistral-nemo)- [deepseek/deepseek-r1](/deepseek/deepseek-r1)- [meta-llama/llama-3.1-70b-instruct](/meta-llama/llama-3.1-70b-instruct)- [meta-llama/llama-3.1-405b-instruct](/meta-llama/llama-3.1-405b-instruct)- [mistralai/mixtral-8x22b-instruct](/mistralai/mixtral-8x22b-instruct)- [cohere/command-r-plus](/cohere/command-r-plus)- [cohere/command-r](/cohere/command-r)"
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
