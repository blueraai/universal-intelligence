from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.openrouter_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.openrouter_text_to_text.meta import generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.openrouter_text_to_text.types import InferenceConfiguration


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "allenai/olmo-7b-instruct"
    _description: ClassVar[str] = (
        "OLMo 7B Instruct by the Allen Institute for AI is a model finetuned for question answering. It demonstrates **notable performance** across multiple benchmarks including TruthfulQA and ToxiGen.**Open Source**: The model, its code, checkpoints, logs are released under the [Apache 2.0 license](https://choosealicense.com/licenses/apache-2.0).- [Core repo (training, inference, fine-tuning etc.)](https://github.com/allenai/OLMo)- [Evaluation code](https://github.com/allenai/OLMo-Eval)- [Further fine-tuning code](https://github.com/allenai/open-instruct)- [Paper](https://arxiv.org/abs/2402.00838)- [Technical blog post](https://blog.allenai.org/olmo-open-language-model-87ccfc95f580)- [W&B Logs](https://wandb.ai/ai2-llm/OLMo-7B/reports/OLMo-7B--Vmlldzo2NzQyMzk5)"
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
