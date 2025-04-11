from typing import ClassVar

from ....core.universal_tool import AbstractUniversalTool
from ....core.utils.types import Contract, Requirement


class UniversalTool(AbstractUniversalTool):
    _contract: ClassVar[Contract] = {
        "name": "Simple Printer",
        "description": "Prints a given text to the console",
        "methods": [
            {
                "name": "print_text",
                "description": "Prints to the console",
                "arguments": [
                    {
                        "name": "text",
                        "type": "str",
                        "schema": {"maxLength": 100},
                        "description": "Text to be printed",
                        "required": True,
                    }
                ],
                "outputs": [
                    {
                        "value_type": "str",
                        "description": "Text printed in the console",
                        "required": True,
                    },
                    {
                        "value_type": "dict",
                        "description": "Status of the operation",
                        "required": True,
                    }
                ],
            },
            {
                "name": "contract",
                "description": "Get a copy of the tool's contract specification, which describes its capabilities, methods, and interfaces. This helps understand what functionality the tool provides.",
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
                "description": "Get a copy of the tool's configuration requirements, detailing what credentials and settings are needed to use this tool. This helps ensure proper tool setup.",
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

    _requirements: ClassVar[list[Requirement]] = [
        {
            "name": "prefix",
            "type": "str",
            "schema": {},
            "description": "Prefix for the example tool logs",
            "required": False,
        }
    ]

    @classmethod
    def contract(cls) -> Contract:
        return cls._contract.copy()

    @classmethod
    def requirements(cls) -> list[Requirement]:
        return cls._requirements.copy()

    def __init__(self, configuration: dict | None = None) -> None:
        self._configuration = configuration if configuration is not None else {}

    def print_text(self, text: str) -> tuple[str, dict]:
        print("\n\n\n")
        if "prefix" in self._configuration:
            print(f"[{self._configuration['prefix']}] {text}")
        else:
            print(text)
        print("\n\n\n")
        return text, { "status": "success" }
