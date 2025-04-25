"""
Test script for model configurations.

To run this script from the project root run:
   python -m universal_intelligence..<model_name>.test
"""

from ..__utils__.test import run_all_tests
from .model import UniversalModel

if __name__ == "__main__":
    run_all_tests(UniversalModel)
