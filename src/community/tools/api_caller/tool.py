import random
import time
from typing import Any, ClassVar

import requests

from src.core.universal_tool import AbstractUniversalTool
from src.core.utils.types import Contract, Requirement


class UniversalTool(AbstractUniversalTool):
    _contract: ClassVar[Contract] = {
        "name": "API Caller",
        "description": "Makes HTTP requests to an API endpoint",
        "methods": [
            {
                "name": "call_api",
                "description": "Makes an HTTP request to an API endpoint",
                "arguments": [
                    {
                        "name": "url",
                        "type": "str",
                        "schema": {},
                        "description": "API endpoint URL",
                        "required": True,
                    },
                    {
                        "name": "method",
                        "type": "str",
                        "schema": {"enum": ["GET", "POST", "PUT", "DELETE", "PATCH"]},
                        "description": "HTTP method to use",
                        "required": False,
                    },
                    {
                        "name": "body",
                        "type": "dict",
                        "schema": {},
                        "description": "Request body for POST/PUT/PATCH requests",
                        "required": False,
                    },
                    {
                        "name": "params",
                        "type": "dict",
                        "schema": {},
                        "description": "Query parameters for the request",
                        "required": False,
                    },
                    {
                        "name": "headers",
                        "type": "dict",
                        "schema": {},
                        "description": "Additional headers to include in the request",
                        "required": False,
                    },
                    {
                        "name": "timeout",
                        "type": "int",
                        "schema": {},
                        "description": "Timeout for the request in seconds",
                        "required": False,
                    },
                ],
                "outputs": [
                    {
                        "value_type": "dict",
                        "description": "API response with status code and data",
                        "required": True,
                    }
                ],
            },
            {
                "name": "contract",
                "description": "Get a copy of the tool's contract specification",
                "arguments": [],
                "outputs": [
                    {
                        "type": "Contract",
                        "schema": {},
                        "description": "A copy of the tool's contract specification",
                        "required": True,
                    }
                ],
            },
            {
                "name": "requirements",
                "description": "Get a copy of the tool's configuration requirements",
                "arguments": [],
                "outputs": [
                    {
                        "type": "List[Requirement]",
                        "schema": {},
                        "description": "A list of the tool's configuration requirements",
                        "required": True,
                    }
                ],
            },
        ],
    }

    _requirements: ClassVar[list[Requirement]] = []

    @classmethod
    def contract(cls) -> Contract:
        return cls._contract.copy()

    @classmethod
    def requirements(cls) -> list[Requirement]:
        return cls._requirements.copy()

    def __init__(self, configuration: dict | None = None) -> None:
        self._configuration = configuration if configuration is not None else {}
        self._default_headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        self._last_request_time = 0
        self._min_request_interval = 2  # Minimum seconds between requests

    def call_api(
        self,
        url: str,
        method: str = "GET",
        body: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        timeout: int | None = None,
    ) -> dict[str, Any]:
        # Throttle requests to avoid rate limiting
        current_time = time.time()
        time_since_last_request = current_time - self._last_request_time
        if time_since_last_request < self._min_request_interval:
            time.sleep(self._min_request_interval - time_since_last_request + random.uniform(0.5, 1.5))

        # Merge default headers with request-specific headers
        request_headers = self._default_headers.copy()
        if headers:
            request_headers.update(headers)

        try:
            response = requests.request(
                method=method,
                url=url,
                json=body,
                params=params,
                headers=request_headers,
                timeout=timeout if timeout is not None else 30,
            )

            self._last_request_time = time.time()

            # Try to parse JSON response, but handle non-JSON responses gracefully
            try:
                data = response.json() if response.text else None
            except ValueError as e:
                data = {
                    "raw_response": response.text,
                    "error": f"Failed to parse JSON response: {e!s}",
                }

            return {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "data": data,
                "raw_response": response.text if not isinstance(data, dict) else None,
            }
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": 500,
                "details": {
                    "url": url,
                    "method": method,
                    "error_type": type(e).__name__,
                },
            }
