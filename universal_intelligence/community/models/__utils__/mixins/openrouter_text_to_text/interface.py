import json
from typing import Any

import requests

from ......community.__utils__.logger import Color, Logger, LogLevel
from ......core.universal_model import AbstractUniversalModel
from ......core.utils.types import Message
from .types import InferenceConfiguration


class UniversalModelMixin(AbstractUniversalModel):

    def __init__(
        self,
        interface_config: dict,
        credentials: str | dict | None = None,
        verbose: bool | str = "DEFAULT",
    ) -> None:
        """Initialize the model with specified engine and configuration."""
        self._log_level = LogLevel.NONE
        if verbose:
            if isinstance(verbose, bool):
                self._log_level = LogLevel.DEFAULT if verbose else LogLevel.NONE
            elif isinstance(verbose, str) and verbose.upper() in LogLevel.__members__:
                self._log_level = LogLevel[verbose.upper()]
            else:
                raise ValueError(f"Invalid verbose value: {verbose} (must be bool or str)")

        with Logger(self._log_level) as logger:

            if not interface_config["name"]:
                raise ValueError("[UniversalModelMixin:__init__:interface_config] Name is not implemented")
            if not interface_config["inference_configuration"]:
                raise ValueError("[UniversalModelMixin:__init__:interface_config] Inference configuration is not implemented")

            logger.print(message=f'* Initializing model.. ({interface_config["name"]}) *\n', color=Color.WHITE)

            # Validate credentials
            logger.print(prefix="Credentials", message="Validating credentials..")
            if credentials:
                if isinstance(credentials, str):
                    credentials = {"api_key": credentials}
            else:
                logger.print(prefix="Credentials", message="No credentials provided. Please provide a valid OpenRouter API key.", color=Color.RED)
                raise ValueError("[UniversalModelMixin:__init__:credentials] Missing credentials. Please provide a valid OpenRouter API key.")
            logger.print(prefix="Credentials", message="Credentials found.", color=Color.GREEN)

            # Validate credits
            if not interface_config["name"].endswith(":free"):
                logger.print(prefix="Credentials", message="Validating credits..")

                response = requests.get("https://openrouter.ai/api/v1/credits", headers={"Authorization": f"Bearer {credentials['api_key']}"})
                if response.status_code >= 400:
                    logger.print(prefix="Credentials", message="Invalid credentials. Please provide a valid OpenRouter API key.", color=Color.RED)
                    raise ValueError("[UniversalModelMixin:__init__:credentials] Invalid credentials. Please provide a valid OpenRouter API key.")
                else:
                    if response.json()["data"]["total_credits"] <= 0:
                        logger.print(prefix="Credentials", message="No credit left. Please add credits to your OpenRouter account if you choose to use a paid model.", color=Color.RED)
                        raise ValueError("[UniversalModelMixin:__init__:credentials] No credit left. Please add credits to your OpenRouter account if you choose to use a paid model.")
                    else:
                        logger.print(prefix="Credentials", message=f"Credits: {response.json()['data']['total_credits']}", color=Color.GREEN)
            else:
                logger.print(prefix="Credentials", message="Free model selected. Skipping credit validation.")

            # Store interface config
            logger.print(prefix="Model", message="Setting up model configuration..")
            self._credentials = credentials
            self._inference_configuration: InferenceConfiguration = interface_config["inference_configuration"]
            self.name = interface_config["name"]
            self.engine = "openrouter"

            self.history = []
            logger.print(prefix="Model", message=f"Initialized remote model: {self.name}", color=Color.MAGENTA)
            logger.print(prefix="Model", message=f"Device: cloud, Engine: {self.engine}\n", color=Color.MAGENTA)

    def _translate_generation_config(self, configuration: dict | None = None) -> dict:
        """Translate generation configuration parameters based on engine type."""
        result = self._inference_configuration[self.engine].copy()

        if configuration:
            result.update(configuration)

        # translate to openrouter format
        # Map transformers parameters to OpenRouter format
        openrouter_params = {}

        # temperature -> temperature
        if "temperature" in result:
            openrouter_params["temperature"] = result["temperature"]

        # max_new_tokens -> max_tokens
        if "max_new_tokens" in result:
            openrouter_params["max_tokens"] = result["max_new_tokens"]

        # top_p -> top_p (0-1)
        if "top_p" in result:
            openrouter_params["top_p"] = result["top_p"]

        # top_k -> top_k (minimum 1)
        if "top_k" in result:
            openrouter_params["top_k"] = result["top_k"]

        # presence_penalty -> presence_penalty
        if "presence_penalty" in result:
            openrouter_params["presence_penalty"] = result["presence_penalty"]

        # frequency_penalty -> frequency_penalty
        if "frequency_penalty" in result:
            openrouter_params["frequency_penalty"] = result["frequency_penalty"]

        # repetition_penalty -> repetition_penalty
        if "repetition_penalty" in result:
            openrouter_params["repetition_penalty"] = result["repetition_penalty"]

        # min_p -> min_p
        if "min_p" in result:
            openrouter_params["min_p"] = result["min_p"]

        # top_a -> top_a
        if "top_a" in result:
            openrouter_params["top_a"] = result["top_a"]

        # seed -> seed
        if "seed" in result:
            openrouter_params["seed"] = result["seed"]

        # response_format -> response_format
        if "response_format" in result:
            openrouter_params["response_format"] = result["response_format"]

        # structured_output -> structured_output
        if "structured_output" in result:
            openrouter_params["structured_output"] = result["structured_output"]

        # stop -> stop (array of strings)
        if "stop" in result:
            openrouter_params["stop"] = result["stop"]

        result = openrouter_params

        print(f"\n[Generation Config] Engine: {self.engine}")
        print(f"Input config: {configuration}")
        print(f"Translated config: {result}\n")

        return result

    def process(self, input: str | list[Message], context: list[Any] | None = None, configuration: dict | None = None, remember: bool = False) -> tuple[Any, dict]:
        """Process input through the model."""
        with Logger(self._log_level) as logger:
            logger.print(message=f"* Invoking remote model.. ({self.name}) *\n", color=Color.WHITE)
            if not input:
                raise ValueError("Input is required")

            logger.print(prefix="Model", message="Translating input..", color=Color.GRAY)

            # Convert input to messages format if string
            messages = input if isinstance(input, list) else [{"role": "user", "content": input}]

            # Add context if provided
            if context:
                messages = [{"role": "system", "content": str(ctx)} for ctx in context] + messages

            # Add history to current messages
            if self.history:
                messages = self.history + messages

            logger.print(prefix="Model", message=f"Translated input: {messages}", color=Color.GRAY, debug=True)

            # Translate generation configuration
            logger.print(prefix="Model", message="Translating inference configuration..", color=Color.GRAY)
            generation_config = self._translate_generation_config(configuration)

            logger.print(prefix="Model", message="Generating output..", color=Color.CYAN)

            # Process input through OpenRouter
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self._credentials['api_key']}",
                    "HTTP-Referer": self._credentials["http_referrer"] if "http_referrer" in self._credentials else "",
                    "X-Title": self._credentials["x_title"] if "x_title" in self._credentials else "",
                    "Content-Type": "application/json",
                },
                data=json.dumps({"model": self.name, "messages": messages, **generation_config}),
            )

            if response.status_code >= 400:
                logger.print(prefix="Model", message="Error generating output.", color=Color.RED)
                raise ValueError("[UniversalModelMixin:process] Error generating output.")

            # Extract output from response
            output = (response.json())["choices"][0]["message"]["content"]

            logger.print(prefix="Model", message="Generating output..", color=Color.GRAY, replace_last_line=True)
            logger.print(prefix="Model", message="Generation complete", color=Color.GREEN)

            # Update history if remember is True
            if remember:
                self.history = [*messages, {"role": "assistant", "content": output}]

            logger.print(prefix="Model", message=f"Response: {response}", color=Color.GRAY, debug=True)

            return output, {"engine": self.engine}

    def load(self) -> None:
        """Load model into memory based on engine type."""
        with Logger(self._log_level) as logger:
            logger.print(message=f"* Loading model.. ({self.name}) *", color=Color.WHITE)
            logger.print(prefix="Model", message="No local model to load. Model is remote (cloud-based).", color=Color.YELLOW)

    def unload(self) -> None:
        """Unload model from memory."""
        with Logger(self._log_level) as logger:
            logger.print(message=f"* Unloading model.. ({self.name}) *", color=Color.WHITE)
            logger.print(prefix="Model", message="No local model to unload. Model is remote (cloud-based).", color=Color.YELLOW)

    def loaded(self) -> bool:
        """Check if model is loaded"""
        return self.name is not None

    def configuration(self) -> dict:
        """Get model configuration"""
        with Logger(self._log_level):
            config = {
                "engine": self.engine,
                "inference_config": self._translate_generation_config(),
            }
            return config

    def reset(self) -> None:
        """Reset model chat history."""
        self.history = []
