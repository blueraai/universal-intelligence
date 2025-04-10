from typing import Any, Literal, TypedDict


# Engine configuration types
class EngineConfig(TypedDict):
    name: str
    model_id: str
    model_file: str | None
    is_default: bool


class QuantizationConfig(TypedDict):
    available_engines: list[EngineConfig]
    is_default: bool
    memory: float
    precision: int


Sources = dict[Literal["cuda", "mps", "cpu"], dict[str, QuantizationConfig]]

ModelConfiguration = dict[str, dict[str, Any]]

InferenceConfiguration = dict[str, dict[str, Any]]


class InputProcessorConfig(TypedDict, total=False):
    tokenizer: dict[str, Any]
    chat_template: dict[str, Any]


class ProcessorConfig(TypedDict, total=False):
    input: InputProcessorConfig
    output: dict[str, Any]


ProcessorConfiguration = dict[Literal["transformers", "mlx-lm", "llama.cpp"], ProcessorConfig]


class ChatTemplate(TypedDict):
    system_start: str
    system_end: str
    user_start: str
    user_end: str
    assistant_start: str
    assistant_end: str
    default_system_message: str
    generation_prompt: str


class QuantizationSettings(TypedDict):
    default: str | None
    min_precision: Literal["2bit", "3bit", "4bit", "5bit", "6bit", "8bit", "16bit", "32bit"] | None
    max_precision: Literal["2bit", "3bit", "4bit", "5bit", "6bit", "8bit", "16bit", "32bit"] | None
    max_memory_allocation: float | None
