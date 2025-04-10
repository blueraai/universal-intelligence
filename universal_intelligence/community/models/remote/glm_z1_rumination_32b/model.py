from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "thudm/glm-z1-rumination-32b"
    _description: ClassVar[str] = (
        "THUDM: GLM Z1 Rumination 32B is a 32B-parameter deep reasoning model from the GLM-4-Z1 series, optimized for complex, open-ended tasks requiring prolonged deliberation. It builds upon glm-4-32b-0414 with additional reinforcement learning phases and multi-stage alignment strategies, introducing 'rumination' capabilities designed to emulate extended cognitive processing. This includes iterative reasoning, multi-hop analysis, and tool-augmented workflows such as search, retrieval, and citation-aware synthesis. The model excels in research-style writing, comparative analysis, and intricate question answering. It supports function calling for search and navigation primitives (`search`, `click`, `open`, `finish`), enabling use in agent-style pipelines. Rumination behavior is governed by multi-turn loops with rule-based reward shaping and delayed decision mechanisms, benchmarked against Deep Research frameworks such as OpenAI's internal alignment stacks. This variant is suitable for scenarios requiring depth over speed."
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
