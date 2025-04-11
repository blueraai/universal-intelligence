import gc
import os
from typing import Any

import psutil
import torch
from huggingface_hub import hf_hub_download, whoami
from transformers import AutoModelForCausalLM, AutoTokenizer

from .meta import extract_precision_from_descriptor
from .types import ChatTemplate, InferenceConfiguration, ModelConfiguration, ProcessorConfiguration, QuantizationSettings, Sources
from ......core.universal_model import AbstractUniversalModel
from ......core.utils.types import Message

# Set CUDA memory allocation configuration to use expandable segments
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"


class UniversalModelMixin(AbstractUniversalModel):

    def _get_available_memory(self, device_type: str) -> float:
        """Get available memory in GB for the specified device type."""
        if device_type == "cuda":
            if not torch.cuda.is_available():
                return 0.0

            print("\n[Memory Detection] CUDA Memory Status:")
            total_memory = 0
            for i in range(torch.cuda.device_count()):
                device = torch.cuda.get_device_properties(i)
                device_memory = device.total_memory
                device_allocated = torch.cuda.memory_allocated(i)
                device_cached = torch.cuda.memory_reserved(i)
                device_available = device_memory - device_allocated

                print(f"Device {i} ({device.name}):")
                print(f"  Total: {device_memory / (1024**3):.2f}GB")
                print(f"  Allocated: {device_allocated / (1024**3):.2f}GB")
                print(f"  Cached: {device_cached / (1024**3):.2f}GB")
                print(f"  Available: {device_available / (1024**3):.2f}GB")

                total_memory += device_memory

            total_available = total_memory / (1024**3)
            print(f"Total available across all devices: {total_available:.2f}GB")
            return total_available

        elif device_type == "mps":
            if not torch.backends.mps.is_available():
                return 0.0
            # For MPS, we need to consider both system memory and driver memory
            system_memory = psutil.virtual_memory()
            driver_memory = torch.mps.driver_allocated_memory()

            # Calculate available memory considering both system and driver memory
            # We subtract the driver memory from total system memory to get true available memory
            total_available = (system_memory.available + driver_memory) / (1024**3)

            print("\n[Memory Detection] MPS Memory Status:")
            print(f"System available: {system_memory.available / (1024**3):.2f}GB")
            print(f"Driver allocated: {driver_memory / (1024**3):.2f}GB")
            print(f"Total available: {total_available:.2f}GB")

            return total_available
        else:  # cpu
            system_memory = psutil.virtual_memory()
            print("\n[Memory Detection] CPU Memory Status:")
            print(f"Total: {system_memory.total / (1024**3):.2f}GB")
            print(f"Available: {system_memory.available / (1024**3):.2f}GB")
            print(f"Used: {system_memory.used / (1024**3):.2f}GB")
            return system_memory.available / (1024**3)

    def __init__(
        self,
        interface_config: dict,
        engine: str | list[str] | None = None,
        quantization: str | list[str] | QuantizationSettings | None = None,
        max_memory_allocation: float | None = None,
        configuration: dict | None = None,
    ) -> None:
        """Initialize the model with specified engine and configuration."""
        # Check Hugging Face login status
        try:
            whoami()
        except Exception as e:
            message = f"\n[Warning] Hugging Face login not detected. Some models may require authentication to download.\n"
            message += "To login, run: huggingface-cli login\n"
            message += "For more information, visit: https://huggingface.co/docs/huggingface_hub/quick-start#login\n"
            print(message)
            raise Exception(message)

        if not interface_config["name"]:
            raise ValueError("[UniversalModelMixin:__init__:interface_config] Name is not implemented")
        if not interface_config["sources"]:
            raise ValueError("[UniversalModelMixin:__init__:interface_config] Sources are not implemented")
        if not interface_config["model_configuration"]:
            raise ValueError("[UniversalModelMixin:__init__:interface_config] Model configuration is not implemented")
        if not interface_config["inference_configuration"]:
            raise ValueError("[UniversalModelMixin:__init__:interface_config] Inference configuration is not implemented")
        if not interface_config["processor_configuration"]:
            raise ValueError("[UniversalModelMixin:__init__:interface_config] Processor configuration is not implemented")
        if not interface_config["chat_template"]:
            raise ValueError("[UniversalModelMixin:__init__:interface_config] Chat template is not implemented")

        # Define the interface configuration
        self._name: str = interface_config["name"]
        self._sources: Sources = interface_config["sources"]
        self._model_configuration: ModelConfiguration = interface_config["model_configuration"]
        self._inference_configuration: InferenceConfiguration = interface_config["inference_configuration"]
        self._processor_configuration: ProcessorConfiguration = interface_config["processor_configuration"]
        self._chat_template: ChatTemplate = interface_config["chat_template"]

        # Detect device type
        device_type = "cpu"  # default
        _device_warning = f''
        if torch.cuda.is_available():
            device_type = "cuda"
        elif torch.backends.mps.is_available():
            device_type = "mps"
            print(f"[Memory Status] Tensor bytes allocated: {torch.mps.current_allocated_memory()} | Driver bytes reserved: {torch.mps.driver_allocated_memory()}")
        else:
            _device_warning += '\n[Warning] No compatible GPU device type detected. Using CPU as default.\n[Warning] If running on a compatible device (mps,cuda), please ensure that the correct driver is installed, and that the "universal_intelligence" package is installed with the correct dependencies by running:\n\npip install "universal_intelligence[community,cuda]"\n(or)\npip install "universal_intelligence[community,mps]"\n\n[Warning] See https://github.com/huggingface/universal_intelligence/ for installation instructions.\n'

        print(f"\n[Device Detection] Using device type: {device_type}{_device_warning}")

        # Get device-specific sources
        device_sources = self._sources.get(device_type, self._sources["cpu"])  # fallback to CPU if device not found
        print(f"[Device Sources] Available sources for {device_type}: {list(device_sources.keys())}")

        # Set maximum memory allocation (default: 85% of available memory)
        self.usable_memory = 0.85
        if max_memory_allocation:
            if 0 <= max_memory_allocation <= 1:
                self.usable_memory = max_memory_allocation
                print(f"[Memory Allocation] Using custom max memory allocation: {self.usable_memory * 100}%")
            else:
                raise ValueError(f"Invalid max_memory value: {max_memory_allocation} (percentage must be between 0 and 1 inclusive)")

        # Set quantization based on device-specific defaults or user input
        self.quantization = quantization
        if self.quantization is None:
            print("\n[Quantization Selection] No quantization specified, using automatic selection")
            # Default case - use current logic but cap minimum precision to 4 bit
            default_quant = next(quant for quant, source in device_sources.items() if source.get("is_default", False))
            required_memory = device_sources[default_quant].get("memory", float("inf"))
            available_memory = self._get_available_memory(device_type) * self.usable_memory

            print(f"[Memory Check] Default quantization '{default_quant}' requires {required_memory:.1f}GB, available: {available_memory:.1f}GB")

            # If default quantization fits within 80% of available memory, use it
            if required_memory <= available_memory:
                self.quantization = default_quant
                print(f"[Decision] Using default quantization '{default_quant}' as it fits in available memory")
            else:
                print("[Incompatiblility] Default quantization doesn't fit, searching for alternatives")
                # Otherwise find the largest quantization that fits with minimum 4 bit precision
                quantizations = sorted(
                    device_sources.items(),
                    key=lambda x: x[1].get("memory", float("inf")),
                    reverse=True,
                )
                for quant, source in quantizations:
                    if source.get("precision", 32) >= 4:  # Minimum 4 bit precision
                        required_memory = source.get("memory", float("inf"))
                        if required_memory <= available_memory:
                            self.quantization = quant
                            print(f"[Decision] Found suitable quantization '{quant}' with {source.get('precision', 32)}-bit precision requiring {required_memory:.1f}GB")
                            break
                        else:
                            print(f"[Assesment] Quantization '{quant}' does not fit within available memory")
                    else:
                        print(f"[Assesment] Quantization '{quant}' does not meet minimum 4-bit precision")
                else:
                    raise ValueError(f"No quantization with minimum 4-bit precision found that fits within {self.usable_memory * 100}% of the available memory ({available_memory:.1f}GB)")
        elif isinstance(self.quantization, str):
            print(f"\n[Quantization Selection] Using specified quantization: {self.quantization}")
            # Single string case - use as is, no defaulting
            pass
        elif isinstance(self.quantization, list):
            print(f"\n[Quantization Selection] Trying quantizations from list: {self.quantization}")
            # List case - try each quantization in order
            for quant in self.quantization:
                if quant in device_sources:
                    self.quantization = quant
                    print(f"[Decision] Using quantization '{quant}' from provided list")
                    break
            else:
                raise ValueError(f"No quantization from the provided list {self.quantization} is supported for {device_type}")
        else:  # QuantizationSettings case
            print("\n[Quantization Selection] Using QuantizationSettings configuration")
            # Get min and max precision from settings
            min_precision = 4  # Default minimum
            max_precision = 8  # Default maximum

            if self.quantization.min_precision:
                min_precision = extract_precision_from_descriptor(self.quantization.min_precision)
                print(f"[Precision] Using custom min precision: {min_precision} bits")
            elif self.quantization.default:
                default_quant = self.quantization.default
                if default_quant in device_sources:
                    min_precision = min(4, device_sources[default_quant].get("precision", 32))
                    print(f"[Precision] Using min precision from default quantization '{default_quant}': {min_precision} bits")

            if self.quantization.max_precision:
                max_precision = extract_precision_from_descriptor(self.quantization.max_precision)
                print(f"[Precision] Using custom max precision: {max_precision} bits")
            elif self.quantization.default:
                default_quant = self.quantization.default
                if default_quant in device_sources:
                    max_precision = device_sources[default_quant].get("precision", 32)
                    print(f"[Precision] Using max precision from default quantization '{default_quant}': {max_precision} bits")

            # Find the highest precision quantization that fits within max allowed memory allocation
            available_memory = self._get_available_memory(device_type) * self.usable_memory
            print(f"[Memory Check] Available memory for quantization: {available_memory:.1f}GB")

            quantizations = sorted(
                device_sources.items(),
                key=lambda x: x[1].get("precision", 32),
                reverse=True,
            )

            for quant, source in quantizations:
                precision = source.get("precision", 32)
                if min_precision <= precision <= max_precision:
                    required_memory = source.get("memory", float("inf"))
                    print(f"[Checking] Quantization '{quant}' - Precision: {precision} bits, Required memory: {required_memory:.1f}GB")
                    if required_memory <= available_memory:
                        self.quantization = quant
                        print(f"[Decision] Selected quantization '{quant}' with {precision}-bit precision requiring {required_memory:.1f}GB")
                        break
                    else:
                        print(f"[Assesment] Quantization '{quant}' does not fit within available memory")
                else:
                    print(f"[Assesment] Quantization '{quant}' does not meet precision requirements")
            else:
                raise ValueError(f"No quantization found with precision between {min_precision} and {max_precision} bits " f"that fits within {self.usable_memory * 100}% of the available memory ({available_memory:.1f}GB)")

        # Validate quantization is supported for this device
        supported_quantizations = device_sources.keys()
        if self.quantization not in supported_quantizations:
            raise ValueError(f"Quantization {self.quantization} not supported for {device_type}. Use one of {supported_quantizations}")

        # Get available engines for the selected quantization
        available_engines = device_sources[self.quantization]["available_engines"]
        print(f"\n[Engine Selection] Available engines for quantization '{self.quantization}': {[engine['name'] for engine in available_engines]}")

        # Set engine based on user input or default
        self.engine = engine
        if not self.engine:
            # Find the default engine for this quantization
            default_engine = next(
                (engine["name"] for engine in available_engines if engine.get("is_default", False)),
                None,
            )
            if not default_engine:
                # If no default is marked, use the first available engine
                default_engine = available_engines[0]["name"]
            self.engine = default_engine
            print(f"[Decision] Using default engine '{default_engine}' for quantization '{self.quantization}'")
        elif isinstance(self.engine, list):
            print(f"[Engine Selection] Trying engines from list: {self.engine}")
            # If engine is a list, try each engine in order until finding a supported one
            supported_engines = {engine["name"] for engine in available_engines}
            for engine_name in self.engine:
                if engine_name in supported_engines:
                    self.engine = engine_name
                    print(f"[Decision] Using engine '{engine_name}' from provided list")
                    break
            else:
                # If no engine in the list is supported, raise an error
                raise ValueError(f"No engine from the provided list {self.engine} is supported for {device_type} device " f"with quantization {self.quantization}. Use one of {supported_engines}")

        # Validate engine is supported for this device and quantization
        supported_engines = {engine["name"] for engine in available_engines}
        if self.engine not in supported_engines:
            raise ValueError(f"Engine {self.engine} not supported for {device_type} device with quantization {self.quantization}. Use one of {supported_engines}")

        # Store the selected engine configuration for later use
        self.engine_config = next(engine for engine in available_engines if engine["name"] == self.engine)
        print(f"\n[Proceeding] Using engine '{self.engine}' with quantization '{self.quantization}' on {device_type} device\n")

        self.config = configuration or {}
        self.model = None
        self.tokenizer = None
        self.history = []
        print(f"Initializing model: {self._name}")
        print(f"Device: {device_type}, Engine: {self.engine}, Quantization: {self.quantization}, Config: {self.config}")

    def _translate_model_config(self) -> dict:
        """Get the appropriate model configuration based on engine type."""
        # Start with engine-specific base configuration
        config = self._model_configuration[self.engine].copy()

        # Update device-specific settings
        if self.engine == "transformers":
            if torch.cuda.is_available():
                config.update(
                    {
                        "device_map": "auto",
                        "low_cpu_mem_usage": True,
                        "offload_folder": "offload",
                        "offload_state_dict": True,
                        "max_memory": {i: f"{int(torch.cuda.get_device_properties(i).total_memory * self.usable_memory / (1024**3))}GB" for i in range(torch.cuda.device_count())},
                    }
                )
            elif torch.backends.mps.is_available():
                config["device_map"] = "mps"
        elif self.engine == "llama.cpp":
            config["n_threads"] = os.cpu_count()

            # Enable GPU acceleration if CUDA is available
            if torch.cuda.is_available():
                # Set n_gpu_layers to a large number to offload as many layers as possible to GPU
                config["n_gpu_layers"] = 1000  # This will offload all possible layers to GPU
                config["main_gpu"] = 0  # Use the first GPU
                config["tensor_split"] = None  # Let llama.cpp handle tensor splitting
                config["offload_kqv"] = True  # Offload key, query, value tensors to GPU
                config["mul_mat_q"] = True  # Use GPU for matrix multiplication
                config["use_mmap"] = True  # Use memory mapping for faster loading
                config["use_mlock"] = True  # Lock memory to prevent swapping
                config["gpu_layers"] = 1000  # Alternative parameter for GPU layers
                config["gpu_offload"] = True  # Explicitly enable GPU offloading
                config["gpu_offload_kqv"] = True  # Explicitly enable KQV offloading
                config["gpu_offload_mlp"] = True  # Enable MLP offloading
                config["gpu_offload_embed"] = True  # Enable embedding offloading
                config["gpu_offload_output"] = True  # Enable output layer offloading

            # Map known transformers model config parameters to llama.cpp equivalents
            if "model" in self.config:
                param_mapping = {
                    "max_position_embeddings": "n_ctx",
                    "rope_scaling": None,  # not supported
                    "use_cache": None,  # not supported
                }

                for param, value in self.config["model"].items():
                    llama_param = param_mapping.get(param)
                    if llama_param is not None:
                        config[llama_param] = value

        # Update with user-provided model configuration
        if "model" in self.config:
            config.update(self.config["model"])

        print(f"\n[Model Config] Engine: {self.engine}")
        print(f"Input config: {self.config}")
        print(f"Translated config: {config}\n")

        return config

    def _format_chat_prompt(self, messages: list[Message], add_generation_prompt: bool = True) -> str:
        """Format messages according to the model's chat template.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            add_generation_prompt: Whether to add the prompt for generation

        Returns:
            Formatted prompt string
        """
        prompt = ""

        # Handle empty messages
        if not messages:
            # Add default system message if no messages
            prompt += self._chat_template["system_start"] + self._chat_template["default_system_message"] + self._chat_template["system_end"]
            return prompt

        # Format each message according to its role
        for msg in messages:
            role = msg["role"]
            content = msg["content"]

            if role == "system":
                prompt += self._chat_template["system_start"] + content + self._chat_template["system_end"]
            elif role == "user":
                prompt += self._chat_template["user_start"] + content + self._chat_template["user_end"]
            elif role == "assistant":
                prompt += self._chat_template["assistant_start"] + content + self._chat_template["assistant_end"]

        # Add generation prompt if requested
        if add_generation_prompt:
            prompt += self._chat_template["generation_prompt"]

        return prompt

    def _translate_generation_config(self, configuration: dict | None = None) -> dict:
        """Translate generation configuration parameters based on engine type."""
        result = None

        if not configuration:
            # Use default configurations from _inference_configuration
            result = self._inference_configuration[self.engine].copy()
        else:
            # Translate provided configuration
            if self.engine == "transformers":
                result = configuration
            elif self.engine == "mlx-lm":
                # Map transformers parameters to mlx-lm parameters
                param_mapping = {
                    "max_new_tokens": "max_tokens",
                    "temperature": "temp",  # mlx-lm uses temp
                    "top_p": "top_p",
                    "top_k": "top_k",
                }
                translated = {}
                for key, value in configuration.items():
                    if key in param_mapping:
                        translated[param_mapping[key]] = value
                    else:
                        translated[key] = value
                result = translated
            else:  # llama.cpp
                # Start with default llama.cpp configuration
                result = self._inference_configuration["llama.cpp"].copy()

                if configuration:
                    # Map known transformers parameters to llama.cpp equivalents
                    param_mapping = {
                        "max_new_tokens": "max_tokens",
                        "temperature": "temperature",
                        "top_p": "top_p",
                        "top_k": "top_k",
                        "num_beams": "beam_search_size",
                        "repetition_penalty": "repeat_penalty",
                        "do_sample": None,  # llama.cpp always samples if temperature > 0
                        "early_stopping": None,  # not directly supported
                        "length_penalty": None,  # not directly supported
                        "no_repeat_ngram_size": None,  # not directly supported
                    }

                    for param, value in configuration.items():
                        llama_param = param_mapping.get(param)
                        if llama_param is not None:
                            result[llama_param] = value

                    # Special handling for deterministic generation
                    if configuration.get("do_sample") is False or configuration.get("temperature", 0.1) == 0:
                        result["temperature"] = 0
                        result.pop("top_p", None)  # Remove top_p for deterministic generation

        print(f"\n[Generation Config] Engine: {self.engine}")
        print(f"Input config: {configuration}")
        print(f"Translated config: {result}\n")

        return result

    def process(self, input: str | list[Message], context: list[Any] | None = None, configuration: dict | None = None, remember: bool = False, keep_alive: bool = False) -> tuple[Any, dict]:
        """Process input through the model."""
        if not input:
            raise ValueError("Input is required")

        if not self.model:
            self.load()

        # Convert input to messages format if string
        messages = input if isinstance(input, list) else [{"role": "user", "content": input}]

        # Add context if provided
        if context:
            messages = [{"role": "system", "content": str(ctx)} for ctx in context] + messages

        # Add history to current messages
        if self.history:
            messages = self.history + messages

        # Get processor configurations
        input_processor_config = self._processor_configuration[self.engine]["input"].copy()
        output_processor_config = self._processor_configuration[self.engine]["output"].copy()

        # Update with user-provided processor configurations if available
        if "processor" in self.config:
            if "input" in self.config["processor"]:
                if "tokenizer" in self.config["processor"]["input"]:
                    input_processor_config["tokenizer"].update(self.config["processor"]["input"]["tokenizer"])
                if "chat_template" in self.config["processor"]["input"]:
                    input_processor_config["chat_template"].update(self.config["processor"]["input"]["chat_template"])
            if "output" in self.config["processor"]:
                output_processor_config.update(self.config["processor"]["output"])

        # Process based on engine
        if self.engine == "transformers":
            # Apply input processor config for tokenization
            input_text = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                **input_processor_config.get("chat_template", {}),
            )
            inputs = self.tokenizer(
                input_text,
                return_tensors="pt",
                **input_processor_config.get("tokenizer", {}),
            ).to(self.model.device)

            gen_config = self._translate_generation_config(configuration)
            outputs = self.model.generate(**inputs, **gen_config)

            # Apply output processor config for decoding
            response = self.tokenizer.decode(
                outputs[0][len(inputs.input_ids[0]) :],
                skip_special_tokens=True,
                **output_processor_config,
            )

        elif self.engine == "mlx-lm":
            from mlx_lm import generate
            from mlx_lm.sample_utils import make_sampler

            # Convert messages to prompt using chat template if available
            if hasattr(self.tokenizer, "apply_chat_template") and self.tokenizer.chat_template is not None:
                input_text = self.tokenizer.apply_chat_template(
                    messages,
                    tokenize=False,
                    **input_processor_config.get("chat_template", {}),
                )
            else:
                # Fallback to simple concatenation if no chat template
                input_text = "\n".join(msg["content"] for msg in messages)

            # Configure generation parameters
            gen_config = self._translate_generation_config(configuration)

            # Extract parameters for sampler and generate
            max_tokens = gen_config.get("max_tokens", 2500)
            temp = gen_config.get("temp", 0.1)
            top_p = gen_config.get("top_p", 0.9)

            # Create sampler with temperature and top_p
            sampler = make_sampler(temp, top_p=top_p)

            # Build generation kwargs
            generate_kwargs = {
                "verbose": True,
                "sampler": sampler,
                "max_tokens": max_tokens,
            }

            # Only add stop and stop_tokens if present in gen_config
            if "stop" in gen_config:
                generate_kwargs["stop"] = gen_config["stop"]
            if "stop_tokens" in gen_config:
                generate_kwargs["stop_tokens"] = gen_config["stop_tokens"]

            response = generate(self.model, self.tokenizer, prompt=input_text, **generate_kwargs)

        else:  # llama.cpp
            # Format the prompt using the chat template
            prompt = self._format_chat_prompt(messages)

            # Configure generation parameters
            gen_config = self._translate_generation_config(configuration)

            response = self.model(prompt, **gen_config)["choices"][0]["text"].strip()

        if not keep_alive:
            self.unload()

        # Update history if remember is True
        if remember:
            self.history = [*messages, {"role": "assistant", "content": response}]

        return response, {"engine": self.engine, "quantization": self.quantization}

    def load(self) -> None:
        """Load model into memory based on engine type."""
        # Clear CUDA cache and reset memory stats if CUDA is available
        if torch.cuda.is_available():
            for i in range(torch.cuda.device_count()):
                torch.cuda.empty_cache()
                torch.cuda.reset_peak_memory_stats(i)
                torch.cuda.reset_accumulated_memory_stats(i)
                # Cap available memory for each GPU
                torch.cuda.set_per_process_memory_fraction(self.usable_memory, i)

        if self.engine == "transformers":
            model_id = self.engine_config["model_id"]

            # Get tokenizer config from default and user processor settings
            tokenizer_config = self._processor_configuration[self.engine]["input"]["tokenizer"].copy()
            if "processor" in self.config and "input" in self.config["processor"] and "tokenizer" in self.config["processor"]["input"]:
                tokenizer_config.update(self.config["processor"]["input"]["tokenizer"])

            # Extract and remove special tokens configuration
            special_tokens = tokenizer_config.pop("special_tokens", {})

            # Initialize tokenizer with remaining config
            self.tokenizer = AutoTokenizer.from_pretrained(model_id, **tokenizer_config)

            # Add special tokens if provided
            if special_tokens:
                self.tokenizer.add_special_tokens(special_tokens)
                # Update processor configuration to remove special_tokens
                if "special_tokens" in self._processor_configuration[self.engine]["input"]["tokenizer"]:
                    del self._processor_configuration[self.engine]["input"]["tokenizer"]["special_tokens"]

            # Load model with memory-efficient settings
            model_config = self._translate_model_config()

            self.model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True, **model_config)

        elif self.engine == "mlx-lm":
            from mlx_lm import load

            model_id = self.engine_config["model_id"]

            # Get tokenizer config from default and user processor settings
            tokenizer_config = self._processor_configuration[self.engine]["input"]["tokenizer"].copy()
            if "processor" in self.config and "input" in self.config["processor"] and "tokenizer" in self.config["processor"]["input"]:
                tokenizer_config.update(self.config["processor"]["input"]["tokenizer"])

            self.model, self.tokenizer = load(model_id, tokenizer_config=tokenizer_config)

        else:  # llama.cpp
            from llama_cpp import Llama

            # Download the GGUF model from HuggingFace
            model_id = self.engine_config["model_id"]
            model_file = self.engine_config["model_file"]
            model_path = hf_hub_download(repo_id=model_id, filename=model_file, repo_type="model")

            self.model = Llama(model_path=model_path, **self._translate_model_config())

        # Final memory cleanup
        if torch.cuda.is_available():
            for i in range(torch.cuda.device_count()):
                torch.cuda.empty_cache()
                torch.cuda.reset_peak_memory_stats(i)
                torch.cuda.reset_accumulated_memory_stats(i)

    def unload(self) -> None:
        """Unload model from memory."""
        # Clear any cached tensors and move model to CPU if needed
        if self.model:
            # Clear any cached tensors
            if hasattr(self.model, "clear_cache"):
                self.model.clear_cache()

            # Delete model and force garbage collection
            del self.model
            self.model = None
            gc.collect()

        if self.tokenizer:
            del self.tokenizer
            self.tokenizer = None
            gc.collect()

        # Clear memory based on device type
        if torch.cuda.is_available():
            for i in range(torch.cuda.device_count()):
                # Reset memory stats first
                torch.cuda.reset_peak_memory_stats(i)
                torch.cuda.reset_accumulated_memory_stats(i)

                # Clear cache and synchronize
                torch.cuda.empty_cache()
                torch.cuda.synchronize(i)

                # Reset memory stats again after cleanup
                torch.cuda.reset_peak_memory_stats(i)
                torch.cuda.reset_accumulated_memory_stats(i)

                # Force CUDA to release memory
                torch.cuda.set_per_process_memory_fraction(1.0, i)

        elif torch.backends.mps.is_available():
            # For MPS, we need to clear the cache and synchronize
            torch.mps.empty_cache()
            torch.mps.synchronize()

            # Additional MPS-specific cleanup
            if hasattr(torch.mps, "reset_peak_memory_stats"):
                torch.mps.reset_peak_memory_stats()

            # Force garbage collection again after MPS cleanup
            gc.collect()

            # Log memory state after cleanup
            print("\n[Memory Post-Cleanup]")
            print(f"Tensor bytes allocated: {torch.mps.current_allocated_memory()}")
            print(f"Driver bytes reserved: {torch.mps.driver_allocated_memory()}")

            # Note: MPS driver memory may not be immediately released
            print("\n[Memory Note] MPS driver memory may remain allocated until system needs it.")
            print("This is normal behavior and the memory will be reused for future operations.")

        # Final garbage collection with more aggressive settings
        gc.set_threshold(1)  # Temporarily set threshold to minimum
        gc.collect()
        gc.set_threshold(700, 10, 5)  # Reset to default thresholds

        # Reset memory allocation fraction to default for CUDA
        if torch.cuda.is_available():
            for i in range(torch.cuda.device_count()):
                torch.cuda.set_per_process_memory_fraction(self.usable_memory, i)

            # Log memory state after cleanup
            print("\n[Memory Post-Cleanup]")
            for i in range(torch.cuda.device_count()):
                print(f"Device {i}:")
                print(f"  Allocated: {torch.cuda.memory_allocated(i) / (1024**3):.2f}GB")
                print(f"  Reserved: {torch.cuda.memory_reserved(i) / (1024**3):.2f}GB")
                print(f"  Max allocated: {torch.cuda.max_memory_allocated(i) / (1024**3):.2f}GB")
                print(f"  Max reserved: {torch.cuda.max_memory_reserved(i) / (1024**3):.2f}GB")

            # Note: CUDA memory management
            print("\n[Memory Note] CUDA memory may remain in reserved pool for efficiency.")
            print("This is normal behavior and allows faster reallocation for future operations.")

    def loaded(self) -> bool:
        """Check if model is loaded"""
        return self.model is not None

    def configuration(self) -> dict:
        """Get model configuration"""
        config = {
            "engine": self.engine,
            "quantization": self.quantization,
            "model_config": self._translate_model_config(),
            "inference_config": self._translate_generation_config(self.configuration),
            "processor_config": self._processor_configuration[self.engine],
        }
        return config

    def reset(self) -> None:
        """Reset model chat history."""
        self.history = []
