import copy
import re

import yaml

from ......core.utils.types import Compatibility, Contract
from .types import Sources


def extract_precision_from_descriptor(precision_descriptor: str) -> int:
    """Extract precision from precision descriptor."""
    if not precision_descriptor.endswith("bit"):
        raise ValueError("Precision descriptor must end with 'bit'")
    return int(precision_descriptor.replace("bit", ""))


def generate_sources_from_yaml(yaml_path: str) -> Sources:
    """Load and parse a sources.yaml file to generate the _sources dictionary.

    Args:
        yaml_path: Path to the sources.yaml file

    Returns:
        Sources dictionary matching the structure required by UniversalModelMixin

    Expected YAML structure:
        model_info:
          name: str
          default_quantization:
            cuda: str  # name of default quantization for cuda
            mps: str   # name of default quantization for mps
            cpu: str   # name of default quantization for cpu

        quantizations:
          quantization_name:
            engine: str
            model_id: str
            model_file: str  # optional
            model_size: float
            supported_devices: List[str]  # must contain valid device types: cuda, mps, cpu

    Raises:
        ValueError: If required sections or fields are missing, or if validation fails
    """
    valid_devices = {"cuda", "mps", "cpu"}

    with open(yaml_path) as f:
        data = yaml.safe_load(f)

    if "model_info" not in data:
        raise ValueError("sources.yaml must contain a model_info section")

    if "quantizations" not in data:
        raise ValueError("sources.yaml must contain a quantizations section")

    # Initialize sources structure
    sources: Sources = {"cuda": {}, "mps": {}, "cpu": {}}

    # Get default quantization for each device type
    default_quantizations = data["model_info"].get("default_quantization", {})

    # Validate default quantizations
    for device, quant in default_quantizations.items():
        if device not in valid_devices:
            raise ValueError(f"Invalid device type in default_quantization: {device}")
        if quant not in data["quantizations"]:
            raise ValueError(f"Default quantization {quant} for {device} not found in quantizations")

    # Process each quantization
    for quant_name, quant_info in data["quantizations"].items():
        # Validate required fields
        required_fields = ["engine", "model_id", "model_size", "supported_devices"]
        missing_fields = [field for field in required_fields if field not in quant_info]
        if missing_fields:
            raise ValueError(f"Quantization {quant_name} is missing required fields: {', '.join(missing_fields)}")

        # Get and validate supported devices
        supported_devices = quant_info.get("supported_devices", [])
        if not supported_devices:
            raise ValueError(f"Quantization {quant_name} must support at least one device type")

        invalid_devices = set(supported_devices) - valid_devices
        if invalid_devices:
            raise ValueError(f"Quantization {quant_name} contains invalid device types: {invalid_devices}")

        # Create engine config
        engine_config = {
            "name": quant_info["engine"],
            "model_id": quant_info["model_id"],
            "is_default": True,  # First engine is default unless overridden
        }

        # Add model_file if present
        if quant_info.get("model_file"):
            engine_config["model_file"] = quant_info["model_file"]

        # Create quantization config
        quant_config = {
            "available_engines": [copy.deepcopy(engine_config)],
            "is_default": False,  # Will be set to True later if it matches device's default
            "memory": float(quant_info["model_size"]),
            "precision": int(re.search(r"\d+", quant_name).group() if re.search(r"\d+", quant_name) else "32"),  # Extract first sequence of consecutive digits or default to 32
        }

        # Add to each supported device
        for device in supported_devices:
            # If quantization already exists for this device, append engine
            if quant_name in sources[device]:
                # New engine is not default since we already have engines
                engine_config_copy = copy.deepcopy(engine_config)
                engine_config_copy["is_default"] = False
                sources[device][quant_name]["available_engines"].append(engine_config_copy)
            else:
                # First engine for this quantization
                sources[device][quant_name] = copy.deepcopy(quant_config)
                # Set as default if it matches device's default quantization
                if device in default_quantizations and default_quantizations[device] == quant_name:
                    sources[device][quant_name]["is_default"] = True

    # Validate exactly one default quantization per device type
    for device in valid_devices:
        default_count = sum(1 for quant in sources[device].values() if quant["is_default"])
        if default_count == 0:
            raise ValueError(f"No default quantization specified for device type: {device}")
        elif default_count > 1:
            raise ValueError(f"Multiple default quantizations specified for device type: {device}")

    return sources


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
                        "name": "engine",
                        "type": "str | List[str]",
                        "schema": {},
                        "description": "Name of the engine to use (e.g. transformers, mlx-lm, llama.cpp) or list of engines in order of priority",
                        "required": False,
                    },
                    {
                        "name": "quantization",
                        "type": "str | List[str] | Dict",
                        "schema": {
                            "nested": [
                                {
                                    "name": "default",
                                    "type": "str",
                                    "schema": {},
                                    "description": "Default quantization method",
                                    "required": False,
                                },
                                {
                                    "name": "min_precision",
                                    "type": "str",
                                    "schema": {},
                                    "description": "Minimum precision requirement (e.g. '4bit')",
                                    "required": False,
                                },
                                {
                                    "name": "max_precision",
                                    "type": "str",
                                    "schema": {},
                                    "description": "Maximum precision requirement (e.g. '8bit')",
                                    "required": False,
                                },
                                {
                                    "name": "max_memory_allocation",
                                    "type": "float",
                                    "schema": {},
                                    "description": "Maximum memory allocation as fraction of available memory",
                                    "required": False,
                                },
                            ]
                        },
                        "description": "Quantization method to use (e.g. bfloat16, Q4_K_M, MLX_4) or list of methods in order of priority, or dictionary of quantization settings",
                        "required": False,
                    },
                    {
                        "name": "max_memory_allocation",
                        "type": "float",
                        "schema": {},
                        "description": "Maximum memory allocation as fraction of available memory",
                        "required": False,
                    },
                    {
                        "name": "configuration",
                        "type": "Dict",
                        "schema": {
                            "nested": [
                                {
                                    "name": "model",
                                    "type": "Dict",
                                    "schema": {},
                                    "description": "Model-specific configuration parameters",
                                    "required": False,
                                },
                                {
                                    "name": "processor",
                                    "type": "Dict",
                                    "schema": {
                                        "nested": [
                                            {
                                                "name": "input",
                                                "type": "Dict",
                                                "schema": {},
                                                "description": "Input processor configuration",
                                                "required": False,
                                            },
                                            {
                                                "name": "output",
                                                "type": "Dict",
                                                "schema": {},
                                                "description": "Output processor configuration",
                                                "required": False,
                                            },
                                        ]
                                    },
                                    "description": "Processor configuration parameters",
                                    "required": False,
                                },
                            ]
                        },
                        "description": "Optional configuration dictionary for model, processor, and other settings",
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
                    {
                        "name": "keep_alive",
                        "type": "bool",
                        "schema": {},
                        "description": "Keep model loaded for faster consecutive interactions",
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
                                            {
                                                "name": "quantization",
                                                "type": "str",
                                                "schema": {"pattern": "^(Q4_K_M|Q8_0|bfloat16)$"},
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


def generate_standard_compatibility(sources: Sources) -> list[Compatibility]:
    """Generate a standard compatibility list for the model."""
    compatibilities = []

    # Process each device type (cuda, mps, cpu)
    for device_type, device_sources in sources.items():
        # Process each quantization method for this device
        for quantization, quant_config in device_sources.items():
            # Get available engines for this quantization
            engines = quant_config["available_engines"]

            # Process each engine
            for engine_config in engines:
                engine = engine_config["name"]

                # Create base compatibility entry
                compatibility: Compatibility = {
                    "engine": engine,
                    "quantization": quantization,
                    "devices": [device_type],
                    "memory": quant_config["memory"],  # Use memory from sources config
                    "dependencies": [],  # Will be populated based on engine
                    "precision": quant_config["precision"],
                }

                # Set dependencies based on engine type
                if engine == "transformers":
                    compatibility["dependencies"] = [
                        "torch",
                        "transformers",
                        "huggingface_hub",
                        "accelerate",
                        "protobuf",
                    ]
                    if quantization.startswith("GPTQ"):
                        compatibility["dependencies"].extend(["auto-gptq", "optimum"])
                    elif quantization.startswith("AWQ"):
                        compatibility["dependencies"].extend(["autoawq", "optimum"])
                    elif quantization.startswith("BNB"):
                        compatibility["dependencies"].extend(["bitsandbytes"])
                elif engine == "mlx-lm":
                    compatibility["dependencies"] = [
                        "torch",
                        "mlx",
                        "mlx-lm",
                        "huggingface_hub",
                        "accelerate",
                        "protobuf",
                    ]
                elif engine == "llama.cpp":
                    compatibility["dependencies"] = [
                        "torch",
                        "llama-cpp-python",
                        "huggingface_hub",
                        "protobuf",
                    ]

                compatibilities.append(compatibility)

    return compatibilities
