from ......core.utils.types import Compatibility, Contract


def generate_standard_contract(name: str, description: str) -> Contract:
    """Generate a standard contract for the model."""
    return {
        "name": name,
        "description": description,
        "methods": [
            {
                "name": "__init__",
                "description": f"Initialize {name} model with specified engine and configuration",
                "arguments": [
                    {
                        "name": "credentials",
                        "type": "str | Dict",
                        "schema": {},
                        "description": "OpenRouter API credentials",
                        "required": True,
                    },
                    {
                        "name": "verbose",
                        "type": "bool | str",
                        "schema": {
                            "enum": [
                                "DEFAULT",
                                "NONE",
                                "INFO",
                                "DEBUG",
                            ]
                        },
                        "description": "Verbose output",
                        "required": False,
                    },
                ],
                "outputs": [
                    {
                        "type": "None",
                        "schema": {},
                        "description": "No return value",
                        "required": True,
                    }
                ],
            },
            {
                "name": "process",
                "description": "Process input through the model",
                "arguments": [
                    {
                        "name": "input",
                        "type": "str | List[Message]",
                        "schema": {
                            "nested": [
                                {
                                    "name": "role",
                                    "type": "str",
                                    "schema": {"pattern": "^(system|user|assistant)$"},
                                    "description": "The role of the message sender",
                                    "required": True,
                                },
                                {
                                    "name": "content",
                                    "type": "str",
                                    "schema": {},
                                    "description": "The content of the message",
                                    "required": True,
                                },
                            ]
                        },
                        "description": "Input string or list of messages in chat format",
                        "required": True,
                    },
                    {
                        "name": "context",
                        "type": "List[Any]",
                        "schema": {},
                        "description": "Optional context items to prepend as system messages",
                        "required": False,
                    },
                    {
                        "name": "configuration",
                        "type": "Dict",
                        "schema": {
                            "nested": [
                                {
                                    "name": "max_new_tokens",
                                    "type": "int",
                                    "schema": {"maxLength": 2048},
                                    "description": "Maximum number of tokens to generate",
                                    "required": False,
                                },
                                {
                                    "name": "temperature",
                                    "type": "float",
                                    "schema": {"pattern": "^[0-9]+(.[0-9]+)?$"},
                                    "description": "Sampling temperature (higher = more random)",
                                    "required": False,
                                },
                                {
                                    "name": "top_p",
                                    "type": "float",
                                    "schema": {"pattern": "^[0-9]+(.[0-9]+)?$"},
                                    "description": "Nucleus sampling probability threshold",
                                    "required": False,
                                },
                                {
                                    "name": "top_k",
                                    "type": "int",
                                    "schema": {"pattern": "^[0-9]+$"},
                                    "description": "Top-k sampling threshold",
                                    "required": False,
                                },
                                {
                                    "name": "do_sample",
                                    "type": "bool",
                                    "schema": {},
                                    "description": "Whether to use sampling (False = greedy)",
                                    "required": False,
                                },
                                {
                                    "name": "repetition_penalty",
                                    "type": "float",
                                    "schema": {"pattern": "^[0-9]+(.[0-9]+)?$"},
                                    "description": "Penalty for repeating tokens",
                                    "required": False,
                                },
                            ]
                        },
                        "description": "Optional generation configuration parameters",
                        "required": False,
                    },
                    {
                        "name": "remember",
                        "type": "bool",
                        "schema": {},
                        "description": "Whether to remember this interaction in history",
                        "required": False,
                    },
                ],
                "outputs": [
                    {
                        "type": "Tuple[str, Dict]",
                        "schema": {
                            "nested": [
                                {
                                    "name": "response",
                                    "type": "str",
                                    "schema": {},
                                    "description": "Generated text response",
                                    "required": True,
                                },
                                {
                                    "name": "logs",
                                    "type": "Dict",
                                    "schema": {
                                        "nested": [
                                            {
                                                "name": "engine",
                                                "type": "str",
                                                "schema": {"pattern": "^(transformers|llama\\.cpp)$"},
                                                "description": "Engine used for generation",
                                                "required": True,
                                            },
                                        ]
                                    },
                                    "description": "Processing logs and metadata",
                                    "required": True,
                                },
                            ]
                        },
                        "description": "Generated response and processing logs",
                        "required": True,
                    }
                ],
            },
            {
                "name": "load",
                "description": "Load model into memory based on engine type",
                "arguments": [],
                "outputs": [
                    {
                        "type": "None",
                        "schema": {},
                        "description": "No return value",
                        "required": True,
                    }
                ],
            },
            {
                "name": "unload",
                "description": "Unload model from memory and free resources",
                "arguments": [],
                "outputs": [
                    {
                        "type": "None",
                        "schema": {},
                        "description": "No return value",
                        "required": True,
                    }
                ],
            },
            {
                "name": "loaded",
                "description": "Check if model is loaded",
                "arguments": [],
                "outputs": [
                    {
                        "type": "bool",
                        "schema": {},
                        "description": "True if model is loaded, False otherwise",
                        "required": True,
                    }
                ],
            },
            {
                "name": "configuration",
                "description": "Get a copy of the model's configuration",
                "arguments": [],
                "outputs": [
                    {
                        "type": "Dict",
                        "schema": {},
                        "description": "A copy of the model's configuration",
                        "required": True,
                    }
                ],
            },
            {
                "name": "reset",
                "description": "Reset model chat history",
                "arguments": [],
                "outputs": [
                    {
                        "type": "None",
                        "schema": {},
                        "description": "No return value",
                        "required": True,
                    }
                ],
            },
            {
                "name": "contract",
                "description": "Get a copy of the model's contract specification, which describes its capabilities, methods, and interfaces. This is useful for programmatically understanding the model's features and requirements.",
                "arguments": [],
                "outputs": [
                    {
                        "type": "Contract",
                        "schema": {},
                        "description": "A copy of the model's contract specification",
                        "required": True,
                    }
                ],
            },
            {
                "name": "compatibility",
                "description": "Get a copy of the model's compatibility specifications, detailing supported engines, quantization methods, devices, memory requirements, and dependencies. This helps determine if the model can run in a given environment.",
                "arguments": [],
                "outputs": [
                    {
                        "type": "List[Compatibility]",
                        "schema": {},
                        "description": "A list of the model's compatibility specifications",
                        "required": True,
                    }
                ],
            },
        ],
    }


def generate_standard_compatibility() -> list[Compatibility]:
    """Generate a standard compatibility list for the model."""
    return [
        {
            "engine": "openrouter",
            "quantization": None,
            "devices": ["cloud"],
            "memory": 0.0,
            "dependencies": [],
            "precision": 32,
        }
    ]
