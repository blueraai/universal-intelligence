"""
Shared test utilities for Universal Agents.
"""

import time
from enum import Enum

import torch

from src.core.universal_agent import AbstractUniversalAgent


class TestStatus(Enum):
    PENDING = "\033[90m[PENDING]"  # Grey
    SUCCESS = "\033[92m[SUCCESS]"  # Green
    FAILURE = "\033[91m[FAILURE]"  # Red


def test_meta_information(agent_class: AbstractUniversalAgent):
    """Test the meta information of the agent class."""
    print("\033[94m" + "\n\n================================================\n\n>> Testing meta information: \n\n" + "\033[0m")

    contract = agent_class.contract()
    requirements = agent_class.requirements()
    compatibility = agent_class.compatibility()

    if contract is None:
        raise ValueError("contract() returned None")
    if requirements is None:
        raise ValueError("requirements() returned None")
    if compatibility is None:
        raise ValueError("compatibility() returned None")

    print("\033[92m" + "\n> [PASSED] Contract, Requirements, and Compatibility checks" + "\033[0m\n\n\n")


def test_agent(agent_class: AbstractUniversalAgent, inference_config=None):
    """Test the agent with given or default configurations."""
    if inference_config is None:
        inference_config = {
            "input": "Hello, how are you?",
            "configuration": {
                "max_new_tokens": 2048,
                "temperature": 0.1,
            },
        }

    print("\033[94m" + f"\n\n================================================\n\n>> Testing agent with configuration: \n\n(inference_config) \n{inference_config}\n\n------------------------------------------------\n\n" + "\033[0m")
    try:
        agent = agent_class()

        # Verify required methods exist
        required_methods = [
            "load",
            "unload",
            "reset",
            "loaded",
            "connect",
            "disconnect",
            "process",
        ]
        for method in required_methods:
            if not hasattr(agent, method):
                raise AttributeError(f"Agent instance is missing required method: {method}")
        print("\033[92m" + "\n> [PASSED] All required methods exist on agent instance" + "\033[0m")

        results, logs = agent.process(**inference_config)
        print("\033[92m" + f"\n\n> [PASSED]: \n\n(output) \n{results}\n\n(logs) \n{logs}\n\n" + "\033[0m")
        # Clean up
        agent.unload()
        del agent
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    except Exception as e:
        print("\033[91m" + f"\n\n> [FAILED] Error: \n\n{e}\n\n" + "\033[0m")
        raise e


def run_all_tests(agent_class: AbstractUniversalAgent, inference_config: dict | None = None):
    """Run all tests for the agent."""
    print("\033[95m" + "\n\n================================================\n\n>> Starting agent tests\n\n" + "\033[0m")

    # Test meta information
    test_meta_information(agent_class)
    time.sleep(2)  # allow time for the user to read the output

    # Test agent functionality
    test_agent(agent_class, inference_config)
