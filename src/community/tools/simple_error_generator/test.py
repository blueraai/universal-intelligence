from src.community.tools.__utils__.test import TestExpectation, run_all_tests

from .tool import UniversalTool

# Run all tests with default configuration
run_all_tests(
    UniversalTool,
    expected_failures={
        "raise_error": TestExpectation(
            should_fail=True,
            expected_error=Exception,  # Expect any Exception. Could be any type or string.
        )
    },
)
