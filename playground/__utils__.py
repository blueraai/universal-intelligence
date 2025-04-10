from typing import Any


def formatted_print(prefix: str, payload: Any, logs: Any = None):
    print(f'\033[32m\n\n{prefix} result: "{payload}"' + (f"\n{prefix} logs: {logs}\033[0m\n\n" if logs is not None else "\033[0m\n\n"))
