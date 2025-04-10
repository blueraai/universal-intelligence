"""
Shared test utilities for Universal Models.
"""

import time
from enum import Enum

import psutil
import torch

from ....core.universal_model import AbstractUniversalModel


class TestStatus(Enum):
    PENDING = "\033[90m[PENDING]"  # Grey
    SUCCESS = "\033[92m[SUCCESS]"  # Green
    FAILURE = "\033[91m[FAILURE]"  # Red


class ConfigurationTracker:
    def __init__(self):
        self.statuses: dict[str, TestStatus] = {}
        self.times: dict[str, float] = {}

    def add_config(self, config: dict):
        config_id = f"{config['engine']}/{config['quantization']}"
        self.statuses[config_id] = TestStatus.PENDING
        self.times[config_id] = 0.0

    def update_status(self, config: dict, status: TestStatus, elapsed_time: float = 0.0):
        config_id = f"{config['engine']}/{config['quantization']}"
        self.statuses[config_id] = status
        self.times[config_id] = elapsed_time

    def print_status_list(self):
        print("\n\nConfiguration Test Status:")
        print("-------------------------")
        for config_id, status in self.statuses.items():
            if status == TestStatus.PENDING:
                print(f"{status.value}: {config_id}\033[0m")
            else:
                print(f"{status.value}({self.times[config_id]:.2f}s): {config_id}\033[0m")
        print("\n")


def test_meta_information(model_class: AbstractUniversalModel):
    """Test the meta information of the model class."""
    print("\033[94m" + "\n\n================================================\n## Testing meta information \n================================================\n" + "\033[0m")

    contract = model_class.contract()
    compatibility = model_class.compatibility()

    if contract is None:
        raise ValueError("contract() returned None")
    if compatibility is None:
        raise ValueError("compatibility() returned None")

    print("\033[92m" + "\n--------------------------------------------------\n [PASSED] Contract and Compatibility checks" + "\033[0m\n--------------------------------------------------\n\n\n")


def get_device_info():
    """Get information about available compute devices and memory."""
    device_info = {
        "type": "cpu",  # default
        "memory_gb": psutil.virtual_memory().total / (1024**3) * 0.9,  # 90% of total RAM
    }

    if torch.cuda.is_available():
        device_info["type"] = "cuda"
        # Sum up memory across all available CUDA devices
        total_memory = sum(torch.cuda.get_device_properties(i).total_memory for i in range(torch.cuda.device_count()))
        device_info["memory_gb"] = total_memory / (1024**3) * 0.9  # 90% of total GPU memory
        device_info["gpu_count"] = torch.cuda.device_count()
    elif torch.backends.mps.is_available():
        device_info["type"] = "mps"
        device_info["memory_gb"] = psutil.virtual_memory().total / (1024**3) * 0.9  # MPS shares system memory

    return device_info


def get_valid_configurations(model_class: AbstractUniversalModel, device_info):
    """Get all valid configurations for the current device, sorted by memory requirements and interleaved by engine."""
    compatibilities = model_class.compatibility()

    # Dictionary to store configurations by engine
    configs_by_engine = {}
    seen_pairs = set()  # To track unique engine-quantization pairs

    for compat in compatibilities:
        # Create configuration identifier
        config_id = f"{compat['engine']}/{compat['quantization']}"

        # Skip if device not supported
        if device_info["type"] not in compat["devices"]:
            print("\033[90m" + f"[SKIPPED] Incompatible requirement: *devices: {compat['devices']} *memory: {compat['memory']} | ({device_info['type']}, {device_info['memory_gb']:.2f}GB) - {config_id}" + "\033[0m")
            continue

        # Skip if memory requirement exceeds available memory
        if compat["memory"] > device_info["memory_gb"]:
            print("\033[90m" + f"[SKIPPED] Incompatible requirement: *devices: {compat['devices']} *memory: {compat['memory']} | ({device_info['type']}, {device_info['memory_gb']:.2f}GB) - {config_id}" + "\033[0m")
            continue

        # Create unique pair identifier
        pair = (compat["engine"], compat["quantization"])
        if pair in seen_pairs:
            print("\033[90m" + f"[SKIPPED] Duplicate configuration: {config_id}" + "\033[0m")
            continue

        seen_pairs.add(pair)

        # Group configurations by engine
        if compat["engine"] not in configs_by_engine:
            configs_by_engine[compat["engine"]] = []

        configs_by_engine[compat["engine"]].append(
            (
                compat["memory"],
                {"engine": compat["engine"], "quantization": compat["quantization"]},
            )
        )

    # Sort configurations within each engine by memory requirement
    for engine in configs_by_engine:
        configs_by_engine[engine].sort(key=lambda x: x[0])

    # If no valid configurations were found, raise an error
    if not configs_by_engine:
        raise ValueError("Incompatible hardware: No valid configurations found for the current device and memory constraints")

    # Interleave configurations from different engines
    valid_configs = []
    max_configs = max(len(configs) for configs in configs_by_engine.values())

    for i in range(max_configs):
        for engine in sorted(configs_by_engine.keys()):
            if i < len(configs_by_engine[engine]):
                valid_configs.append(configs_by_engine[engine][i][1])

    # Print queued configurations in order
    for idx, config in enumerate(valid_configs):
        config_id = f"{config['engine']}/{config['quantization']}"
        memory = next(compat["memory"] for compat in compatibilities if compat["engine"] == config["engine"] and compat["quantization"] == config["quantization"])
        print("\033[95m" + f"[QUEUED {idx+1}/{len(valid_configs)}]: Compatible test: *memory: {memory}GB - {config_id}" + "\033[0m")

    return valid_configs


def test_model(
    model_class: AbstractUniversalModel,
    universal_model_config=None,
    inference_config=None,
    tracker: ConfigurationTracker = None,
):
    """Test the model with given or default configurations."""
    if inference_config is None:
        inference_config = {
            "input": "Hello, how are you?",
            "configuration": {
                "max_new_tokens": 2048,
                "temperature": 0.1,
            },
        }

    print("\033[94m" + f"\n\n================================================\n## Testing configuration: \n\n(universal_model_config) \n{universal_model_config}\n\n(inference_config) \n{inference_config}\n================================================\n\n" + "\033[0m")
    try:
        start_time = time.time()
        model = model_class(**universal_model_config) if universal_model_config else model_class()

        # Verify required methods exist
        required_methods = [
            "load",
            "unload",
            "reset",
            "loaded",
            "configuration",
            "process",
        ]
        for method in required_methods:
            if not hasattr(model, method):
                raise AttributeError(f"Model instance missing required method: {method}")

        results, logs = model.process(**inference_config)
        elapsed_time = time.time() - start_time
        print("\033[92m" + f"\n--------------------------------------------------\n [PASSED]: \n\n(output) \n{results}\n\n(logs) \n{logs}\n\n--------------------------------------------------\n" + "\033[0m")
        # Clean up
        model.unload()
        del model
        if torch.cuda.is_available():
            for i in range(torch.cuda.device_count()):
                torch.cuda.empty_cache()
                torch.cuda.reset_peak_memory_stats(i)
                torch.cuda.reset_accumulated_memory_stats(i)
        if tracker:
            tracker.update_status(universal_model_config, TestStatus.SUCCESS, elapsed_time)
            tracker.print_status_list()
    except Exception as e:
        elapsed_time = time.time() - start_time
        print("\033[91m" + f"\n--------------------------------------------------\n [FAILED] Error: \n\n{e}\n\n--------------------------------------------------\n" + "\033[0m")
        if tracker:
            tracker.update_status(universal_model_config, TestStatus.FAILURE, elapsed_time)
            tracker.print_status_list()
        raise e


def run_all_tests(model_class: AbstractUniversalModel, inference_config: dict | None = None):
    """Run tests for all valid configurations."""
    test_meta_information(model_class)
    time.sleep(2)  # allow time for the user to read the output

    print("\033[94m" + "\n\n================================================\n## Setting up tests\n================================================\n" + "\033[0m")
    device_info = get_device_info()
    print(f"\nDevice Info: {device_info}\n")

    valid_configs = get_valid_configurations(model_class, device_info)
    print(f"\nFound {len(valid_configs)} valid configurations to test\n")

    # Initialize the configuration tracker
    tracker = ConfigurationTracker()
    for config in valid_configs:
        tracker.add_config(config)
    tracker.print_status_list()

    time.sleep(2)  # allow time for the user to read the output

    for config in valid_configs:
        print(f"\nTesting configuration: {config}")
        test_model(
            model_class,
            universal_model_config=config,
            inference_config=inference_config,
            tracker=tracker,
        )
