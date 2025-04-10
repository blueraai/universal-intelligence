from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "perplexity/sonar-deep-research"
    _description: ClassVar[str] = (
        "Sonar Deep Research is a research-focused model designed for multi-step retrieval, synthesis, and reasoning across complex topics. It autonomously searches, reads, and evaluates sources, refining its approach as it gathers information. This enables comprehensive report generation across domains like finance, technology, health, and current events. Notes on Pricing ([Source](https://docs.perplexity.ai/guides/pricing#detailed-pricing-breakdown-for-sonar-deep-research)) - Input tokens comprise of Prompt tokens (user prompt) + Citation tokens (these are processed tokens from running searches)- Deep Research runs multiple searches to conduct exhaustive research. Searches are priced at $5/1000 searches. A request that does 30 searches will cost $0.15 in this step.- Reasoning is a distinct step in Deep Research since it does extensive automated reasoning through all the material it gathers during its research phase. Reasoning tokens here are a bit different than the CoTs in the answer - these are tokens that we use to reason through the research material prior to generating the outputs via the CoTs. Reasoning tokens are priced at $3/1M tokens"
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
