from typing import Any, Optional, TypedDict


class Message(TypedDict):
    role: str
    content: Any


class Schema(TypedDict, total=False):
    maxLength: int | None
    pattern: str | None
    minLength: int | None
    nested: list["Argument"] | None
    properties: dict[str, "Schema"] | None
    items: Optional["Schema"]


class Argument(TypedDict):
    name: str
    type: str
    schema: Schema | None
    description: str
    required: bool


class Output(TypedDict):
    type: str
    description: str
    required: bool


class Method(TypedDict):
    name: str
    description: str
    arguments: list[Argument]
    outputs: list[Output]
    asynchronous: bool | None


class Contract(TypedDict):
    name: str
    description: str
    methods: list[Method]


class Requirement(TypedDict):
    name: str
    type: str
    schema: Schema
    description: str
    required: bool


class Compatibility(TypedDict):
    engine: str
    quantization: str
    devices: list[str]
    memory: float
    dependencies: list[str]
    precision: int


class QuantizationSettings(TypedDict):
    default: str | None
    min_precision: str | None
    max_precision: str | None
