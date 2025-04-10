from typing import Any, Literal, TypedDict

# Engine configuration types

ModelConfiguration = dict[str, dict[str, Any]]

InferenceConfiguration = dict[str, dict[str, Any]]


class QuantizationSettings(TypedDict):
    default: str | None
    min_precision: Literal["2bit", "3bit", "4bit", "5bit", "6bit", "8bit", "16bit", "32bit"] | None
    max_precision: Literal["2bit", "3bit", "4bit", "5bit", "6bit", "8bit", "16bit", "32bit"] | None
    max_memory_allocation: float | None
