"""
Test script for Qwen2.5-7B-Instruct model configurations.

To run this script from the project root run:
   python -m src.community.models.qwen2_5_7b_instruct.test
"""

from src.community.models.__utils__.test import run_all_tests

from .model import UniversalModel

if __name__ == "__main__":
    run_all_tests(UniversalModel)
