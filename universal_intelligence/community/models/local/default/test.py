"""
This module contains tests for the default Universal Intelligence model.

The default model is the Qwen2.5-7B-Instruct model.
"""

from ...__utils__.test import run_all_tests
from ..qwen2_5_7b_instruct.model import UniversalModel

if __name__ == "__main__":
    run_all_tests(UniversalModel)
