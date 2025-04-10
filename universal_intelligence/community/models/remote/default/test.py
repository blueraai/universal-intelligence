"""
This module contains tests for the default Universal Intelligence model.

The default model is the auto model selection from OpenRouter.
"""

from ...__utils__.test import run_all_tests
from ..auto.model import UniversalModel

if __name__ == "__main__":
    run_all_tests(UniversalModel)
