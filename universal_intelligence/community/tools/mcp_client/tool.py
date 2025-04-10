from typing import Any, ClassVar

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from ....core.universal_tool import AbstractUniversalTool
from ....core.utils.types import Contract, Requirement


class UniversalTool(AbstractUniversalTool):
    _contract: ClassVar[Contract] = {
        "name": "MCP Client",
        "description": "Calls a tool on a remote MCP server",
        "methods": [
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
            {
                "name": "call_tool",
                "description": "Calls a tool on a remote MCP server",
                "arguments": [
                    {
                        "name": "tool_name",
                        "type": "str",
                        "schema": {"maxLength": 100},
                        "description": "Name of the tool to call",
                        "required": True,
                    },
                    {
                        "name": "arguments",
                        "type": "Dict[str, Any]",
                        "description": "Arguments to pass to the tool",
                        "required": False,
                    },
                ],
                "outputs": [
                    {
                        "value_type": "str",
                        "description": "Result of the tool call",
                        "required": True,
                    },
                    {
                        "value_type": "dict",
                        "description": "Status of the operation",
                        "required": True,
                    },
                ],
                "asynchronous": True,
            },
            {
                "name": "list_prompts",
                "description": "List all available prompts from the MCP server",
                "arguments": [],
                "outputs": [
                    {
                        "type": "List[str]",
                        "schema": {},
                        "description": "A list of available prompts",
                        "required": True,
                    },
                    {
                        "value_type": "dict",
                        "description": "Status of the operation",
                        "required": True,
                    },
                ],
                "asynchronous": True,
            },
            {
                "name": "get_prompt",
                "description": "Get a specific prompt from the MCP server with optional arguments",
                "arguments": [
                    {
                        "name": "prompt_name",
                        "type": "str",
                        "schema": {"maxLength": 100},
                        "description": "Name of the prompt to get",
                        "required": True,
                    },
                    {
                        "name": "arguments",
                        "type": "Dict[str, Any]",
                        "description": "Arguments to pass to the prompt",
                        "required": False,
                    },
                ],
                "outputs": [
                    {
                        "type": "str",
                        "description": "Content of the prompt",
                        "required": True,
                    },
                    {
                        "value_type": "dict",
                        "description": "Status of the operation",
                        "required": True,
                    },
                ],
                "asynchronous": True,
            },
            {
                "name": "list_resources",
                "description": "List all available resources from the MCP server",
                "arguments": [],
                "outputs": [
                    {
                        "type": "List[str]",
                        "schema": {},
                        "description": "A list of available resources",
                        "required": True,
                    },
                    {
                        "value_type": "dict",
                        "description": "Status of the operation",
                        "required": True,
                    },
                ],
                "asynchronous": True,
            },
            {
                "name": "list_tools",
                "description": "List all available tools from the MCP server",
                "arguments": [],
                "outputs": [
                    {
                        "type": "List[str]",
                        "schema": {},
                        "description": "A list of available tools",
                        "required": True,
                    },
                    {
                        "value_type": "dict",
                        "description": "Status of the operation",
                        "required": True,
                    },
                ],
                "asynchronous": True,
            },
            {
                "name": "read_resource",
                "description": "Read a resource from the MCP server and return its content and MIME type",
                "arguments": [
                    {
                        "name": "resource_path",
                        "type": "str",
                        "schema": {"maxLength": 255},
                        "description": "Path to the resource to read",
                        "required": True,
                    }
                ],
                "outputs": [
                    {
                        "type": "Tuple[str, str]",
                        "schema": {
                            "items": [
                                {
                                    "type": "str",
                                    "description": "Content of the resource",
                                },
                                {
                                    "type": "str",
                                    "description": "MIME type of the resource",
                                },
                            ]
                        },
                        "description": "Content and MIME type of the resource",
                        "required": True,
                    },
                    {
                        "value_type": "dict",
                        "description": "Status of the operation",
                        "required": True,
                    },
                ],
                "asynchronous": True,
            },
        ],
    }

    _requirements: ClassVar[list[Requirement]] = [
        {
            "name": "server_command",
            "type": "str",
            "schema": {},
            "description": "Command to execute the MCP server",
            "required": True,
        },
        {
            "name": "server_args",
            "type": "List[str]",
            "schema": {},
            "description": "Command line arguments for the MCP server",
            "required": False,
        },
        {
            "name": "server_env",
            "type": "Dict[str, str]",
            "schema": {},
            "description": "Environment variables for the MCP server",
            "required": False,
        },
    ]

    def __init__(self, configuration: dict[str, Any] | None = None, verbose: str = "DEFAULT") -> None:
        self._configuration = configuration if configuration is not None else {}
        self._session: ClientSession | None = None
        self._verbose = verbose

        # Validate required configuration
        if "server_command" not in self._configuration:
            raise ValueError("server_command is required in configuration")

        self._server_params = StdioServerParameters(
            command=self._configuration["server_command"],
            args=self._configuration.get("server_args", []),
            env=self._configuration.get("server_env"),
        )

    @classmethod
    def contract(cls) -> Contract:
        return cls._contract.copy()

    @classmethod
    def requirements(cls) -> list[Requirement]:
        return cls._requirements.copy()

    async def _initialize_session(self):
        if self._session is None:
            async with stdio_client(self._server_params) as (read, write):
                self._session = ClientSession(read, write)
                await self._session.initialize()

    async def call_tool(self, tool_name: str, arguments: dict[str, Any] | None = None) -> tuple[str, dict]:
        await self._initialize_session()
        if self._session:
            return await self._session.call_tool(tool_name, arguments or {}), {"status": "success"}
        return None, {"status": "error"}

    async def list_prompts(self) -> tuple[list[str], dict]:
        """List all available prompts from the MCP server."""
        await self._initialize_session()
        if self._session:
            return await self._session.list_prompts(), {"status": "success"}
        return [], {"status": "error"}

    async def get_prompt(self, prompt_name: str, arguments: dict[str, Any] | None = None) -> tuple[str, dict]:
        """Get a specific prompt from the MCP server with optional arguments."""
        await self._initialize_session()
        if self._session:
            return await self._session.get_prompt(prompt_name, arguments or {}), {"status": "success"}
        return None, {"status": "error"}

    async def list_resources(self) -> tuple[list[str], dict]:
        """List all available resources from the MCP server."""
        await self._initialize_session()
        if self._session:
            return await self._session.list_resources(), {"status": "success"}
        return [], {"status": "error"}

    async def list_tools(self) -> tuple[list[str], dict]:
        """List all available tools from the MCP server."""
        await self._initialize_session()
        if self._session:
            return await self._session.list_tools(), {"status": "success"}
        return [], {"status": "error"}

    async def read_resource(self, resource_path: str) -> tuple[tuple[str, str], dict]:
        """Read a resource from the MCP server and return its content and MIME type."""
        await self._initialize_session()
        if self._session:
            return (await self._session.read_resource(resource_path)), {"status": "success"}
        return (None, None), {"status": "error"}

    async def __aenter__(self):
        await self._initialize_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            await self._session.close()
            self._session = None
