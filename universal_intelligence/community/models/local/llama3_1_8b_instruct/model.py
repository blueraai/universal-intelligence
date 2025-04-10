import os
from typing import ClassVar

from .....core.utils.types import Compatibility, Contract
from ...__utils__.mixins.hf_text_to_text.interface import UniversalModelMixin
from ...__utils__.mixins.hf_text_to_text.meta import generate_sources_from_yaml, generate_standard_compatibility, generate_standard_contract
from ...__utils__.mixins.hf_text_to_text.types import ChatTemplate, InferenceConfiguration, ModelConfiguration, ProcessorConfiguration, Sources


class UniversalModel(UniversalModelMixin):
    _name: ClassVar[str] = "Llama-3.1-8B-Instruct"
    _description: ClassVar[str] = "An 8B parameter language model from Meta, optimized for instruction following and general language tasks"

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
        "mlx-lm": {"max_tokens": 2500, "temp": 0.1},
        "llama.cpp": {
            "max_tokens": 2500,
            "temperature": 0.1,
            "top_p": 0.9,
            "stream": False,
            "echo": False,
            "stop": ["<|eot_id|>", "<|begin_of_text|>"],
            "repeat_penalty": 1.1,
        },
    }

    _processor_configuration: ClassVar[ProcessorConfiguration] = {
        "transformers": {
            "input": {
                "tokenizer": {
                    # "trust_remote_code": True,
                    # "padding": True,
                    "truncation": True,
                    "return_attention_mask": True,
                    "special_tokens": {
                        "pad_token": "<|eot_id|>",
                        "eos_token": "<|eot_id|>",
                        "bos_token": "<|begin_of_text|>",
                    },
                },
                "chat_template": {"add_generation_prompt": True},
            },
            "output": {
                # "skip_special_tokens": True,
                "clean_up_tokenization_spaces": True
            },
        },
        "mlx-lm": {
            "input": {
                "tokenizer": {"trust_remote_code": True, "eos_token": "<|endoftext|>"},
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
        "system_start": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nCutting Knowledge Date: December 2023\nToday Date: 26 Jul 2024\n\n",
        "system_end": "<|eot_id|>",
        "user_start": "<|start_header_id|>user<|end_header_id|>\n\n",
        "user_end": "<|eot_id|>",
        "assistant_start": "<|start_header_id|>assistant<|end_header_id|>\n\n",
        "assistant_end": "<|eot_id|>",
        "default_system_message": "You are a helpful AI assistant.",
        "generation_prompt": "<|start_header_id|>assistant<|end_header_id|>\n\n",  # Prompt to start generation
    }

    def __init__(self, *args, **kwargs) -> None:
        """Initialize model with specified engine and configuration."""
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
