from typing import Any


def formatted_print(prefix: str, payload: Any, logs: Any = None):
    print(f'\033[90m\n\n{prefix} result: \033[0m\n\033[37m"{payload}\033[0m"' + (f"\n\n\033[90m{prefix} logs:\033[0m \n\033[37m{logs}\033[0m\n\n" if logs is not None else "\033[0m\n\n"))
