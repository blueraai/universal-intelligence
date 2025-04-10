"""
Shared test utilities for Universal Tools.
"""

import time
from enum import Enum

from src.core.universal_tool import AbstractUniversalTool


class TestStatus(Enum):
    PENDING = "\033[90m[PENDING]"  # Grey
    SUCCESS = "\033[92m[SUCCESS]"  # Green
    FAILURE = "\033[91m[FAILURE]"  # Red
    EXPECTED_FAILURE = "\033[93m[EXPECTED FAILURE]"  # Yellow


class TestExpectation:
    def __init__(self, should_fail: bool = False, expected_error: str | type | None = None):
        self.should_fail = should_fail
        self.expected_error = expected_error


class MethodTracker:
    def __init__(self):
        self.statuses: dict[str, TestStatus] = {}
        self.expectations: dict[str, TestExpectation] = {}

    def add_method(self, method_name: str, expectation: TestExpectation = None):
        self.statuses[method_name] = TestStatus.PENDING
        if expectation:
            self.expectations[method_name] = expectation

    def update_status(self, method_name: str, status: TestStatus):
        self.statuses[method_name] = status

    def print_status_list(self):
        print("\n\nTool Method Test Status:")
        print("-------------------------")
        for method_name, status in self.statuses.items():
            expectation = self.expectations.get(method_name)
            expected_str = " (Expected to fail)" if expectation and expectation.should_fail else ""
            print(f"{status.value}: {method_name}{expected_str}\033[0m")
        print("\n")


def test_meta_information(tool_class: AbstractUniversalTool):
    """Test the meta information of the tool class."""
    print("\033[94m" + "\n\n================================================\n\n>> Testing meta information: \n\n" + "\033[0m")

    contract = tool_class.contract()
    requirements = tool_class.requirements()

    if contract is None:
        raise ValueError("contract() returned None")
    if requirements is None:
        raise ValueError("requirements() returned None")

    print("\033[92m" + "\n> [PASSED] Contract and Requirements checks" + "\033[0m\n\n\n")


def test_tool_method(
    tool: AbstractUniversalTool,
    method_name: str,
    test_args: dict,
    tracker: MethodTracker = None,
):
    """Test a specific tool method with given arguments."""
    print("\033[94m" + f"\n\n================================================\n\n>> Testing method: {method_name}\n\nArguments:\n{test_args}\n\n------------------------------------------------\n\n" + "\033[0m")

    expectation = tracker.expectations.get(method_name) if tracker else None

    try:
        method = getattr(tool, method_name)
        result, _ = method(**test_args)

        if expectation and expectation.should_fail:
            print("\033[91m" + f"\n\n> [UNEXPECTED PASS]: Method succeeded but was expected to fail\n\n(output) \n{result}\n\n" + "\033[0m")
            if tracker:
                tracker.update_status(method_name, TestStatus.FAILURE)
                tracker.print_status_list()
            raise AssertionError(f"Method {method_name} succeeded but was expected to fail")

        print("\033[92m" + f"\n\n> [PASSED]: \n\n(output) \n{result}\n\n" + "\033[0m")
        if tracker:
            tracker.update_status(method_name, TestStatus.SUCCESS)
            tracker.print_status_list()

    except Exception as e:
        if expectation and expectation.should_fail:
            if expectation.expected_error:
                if isinstance(expectation.expected_error, str) and str(e) != expectation.expected_error:
                    print("\033[91m" + f"\n\n> [WRONG ERROR]: Expected error '{expectation.expected_error}' but got '{e!s}'\n\n" + "\033[0m")
                    if tracker:
                        tracker.update_status(method_name, TestStatus.FAILURE)
                        tracker.print_status_list()
                    raise
                elif isinstance(expectation.expected_error, type) and not isinstance(e, expectation.expected_error):
                    print("\033[91m" + f"\n\n> [WRONG ERROR TYPE]: Expected error type {expectation.expected_error.__name__} but got {type(e).__name__}\n\n" + "\033[0m")
                    if tracker:
                        tracker.update_status(method_name, TestStatus.FAILURE)
                        tracker.print_status_list()
                    raise

            print("\033[93m" + f"\n\n> [EXPECTED FAILURE]: \n\n(error) \n{e}\n\n" + "\033[0m")
            if tracker:
                tracker.update_status(method_name, TestStatus.EXPECTED_FAILURE)
                tracker.print_status_list()
            return

        print("\033[91m" + f"\n\n> [FAILED] Error: \n\n{e}\n\n" + "\033[0m")
        if tracker:
            tracker.update_status(method_name, TestStatus.FAILURE)
            tracker.print_status_list()
        raise


def get_test_arguments(method_spec: dict) -> dict:
    """Generate test arguments for a method based on its specification."""
    test_args = {}
    for arg in method_spec.get("arguments", []):
        if arg["type"] == "str":
            test_args[arg["name"]] = "Test input string"
        elif arg["type"] == "int":
            test_args[arg["name"]] = 42
        elif arg["type"] == "float":
            test_args[arg["name"]] = 3.14
        elif arg["type"] == "bool":
            test_args[arg["name"]] = True
        elif arg["type"] == "list":
            test_args[arg["name"]] = []
        elif arg["type"] == "dict":
            test_args[arg["name"]] = {}
    return test_args


def run_all_tests(
    tool_class: AbstractUniversalTool,
    tool_config: dict | None = None,
    expected_failures: dict[str, TestExpectation] | None = None,
):
    """
    Run tests for all methods in the tool.

    Args:
        tool_class: The tool class to test
        tool_config: Optional configuration for the tool
        expected_failures: Dictionary mapping method names to their test expectations
    """
    test_meta_information(tool_class)
    time.sleep(2)  # allow time for the user to read the output

    print("\033[94m" + "\n\n================================================\n\n>> Setting up tool tests\n\n" + "\033[0m")

    # Create tool instance
    tool = tool_class(configuration=tool_config) if tool_config else tool_class()

    # Get contract to find all methods
    contract = tool.contract()
    methods = [method for method in contract["methods"] if method["name"] not in ["contract", "requirements"]]

    print(f"\nFound {len(methods)} methods to test\n")

    # Initialize the method tracker
    tracker = MethodTracker()
    for method in methods:
        expectation = expected_failures.get(method["name"]) if expected_failures else None
        tracker.add_method(method["name"], expectation)
    tracker.print_status_list()

    time.sleep(2)  # allow time for the user to read the output

    # Test each method
    for method in methods:
        print(f"\nTesting method: {method['name']}")
        test_args = get_test_arguments(method)
        test_tool_method(tool, method["name"], test_args, tracker)
