import os
from typing import ClassVar

from ....core.utils.types import Compatibility, Contract
from ..__utils__.mixins.text_to_text.interface import UniversalModelMixin
from ..__utils__.mixins.text_to_text.meta import generate_sources_from_yaml, generate_standard_compatibility, generate_standard_contract
from ..__utils__.mixins.text_to_text.types import ChatTemplate, InferenceConfiguration, ModelConfiguration, ProcessorConfiguration, Sources


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "gemma-3-27b-it"
    _description: ClassVar[str] = "A 27B parameter language model from Google, optimized for instruction following and general language tasks"

    _model_configuration: ClassVar[ModelConfiguration] = {
        "transformers": {"device_map": "auto", "torch_dtype": "auto"},
        "mlx-lm": {},  # MLX automatically uses Metal backend on Apple Silicon
        "llama.cpp": {
            "n_ctx": 2048,
            "n_threads": None,  # Will be set to os.cpu_count() at runtime
        },
    }

    _inference_configuration: ClassVar[InferenceConfiguration] = {
        "transformers": {"max_new_tokens": 2500, "temperature": 0.1},
        "mlx-lm": {
            "max_tokens": 2500,
            "temp": 0.1,
            "stop": ["<end_of_turn>"],  # Stop when it sees the next turn marker
        },
        "llama.cpp": {
            "max_tokens": 2500,
            "temperature": 0.1,
            "top_p": 0.9,
            "stream": False,
            "echo": False,
            "stop": ["<bos>", "<start_of_turn>", "<end_of_turn>"],
            "repeat_penalty": 1.1,
        },
    }

    _processor_configuration: ClassVar[ProcessorConfiguration] = {
        "transformers": {
            "input": {
                "tokenizer": {
                    "padding": True,
                    "truncation": True,
                    "return_attention_mask": True,
                },
                "chat_template": {"add_generation_prompt": True},
            },
            "output": {"clean_up_tokenization_spaces": True},
        },
        "mlx-lm": {
            "input": {
                "tokenizer": {"trust_remote_code": True},
                "chat_template": {"add_generation_prompt": True},
            },
            "output": {"skip_special_tokens": True},
        },
        "llama.cpp": {
            "input": {},  # llama.cpp handles input processing internally
            "output": {},  # llama.cpp handles output processing internally
        },
    }

    _chat_template: ClassVar[ChatTemplate] = {
        "system_start": "<bos><start_of_turn>user\n",
        "system_end": "\n\n",
        "user_start": "",  # User message follows directly after system
        "user_end": "<end_of_turn>",  # Removed extra newline
        "assistant_start": "<start_of_turn>model\n",
        "assistant_end": "<end_of_turn>",  # Removed extra newline
        "default_system_message": "You are a helpful AI assistant.",
        "generation_prompt": "<start_of_turn>model\n",  # Prompt to start generation
    }

    def __init__(self, *args, **kwargs) -> None:
        sources_yaml_path = os.path.join(os.path.dirname(__file__), "sources.yaml")
        self._sources: Sources = generate_sources_from_yaml(sources_yaml_path)
        super().__init__(
            interface_config={
                "name": self._name,
                "sources": self._sources,
                "model_configuration": self._model_configuration,
                "inference_configuration": self._inference_configuration,
                "processor_configuration": self._processor_configuration,
                "chat_template": self._chat_template,
            },
            *args,
            **kwargs,
        )

    @classmethod
    def contract(cls) -> Contract:
        return generate_standard_contract(cls._name, cls._description)

    @classmethod
    def compatibility(cls) -> list[Compatibility]:
        return generate_standard_compatibility(cls()._sources)
