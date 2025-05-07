import io
import sys
from dataclasses import dataclass
from enum import Enum
from typing import Any


class Color(Enum):
    """ANSI color codes for terminal output"""

    BLACK = "\033[30m"
    GRAY = "\033[90m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    ORANGE = "\033[38;5;208m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    RESET = "\033[0m"


class LogLevel(Enum):
    """Log levels for controlling output verbosity"""

    NONE = 0  # No output
    DEFAULT = 1  # Default output (no debug messages)
    DEBUG = 2  # All output including debug messages


class LoggerStream(io.TextIOBase):
    """Custom stream to intercept and silence console output"""

    def __init__(self, logger):
        self.logger = logger
        self.buffer = []

    def write(self, text):
        # Only suppress if log level is not DEBUG
        if self.logger._log_level != LogLevel.DEBUG:
            # Just return length without writing anything
            return len(text)
        else:
            # Pass through to original stdout/stderr
            self.logger._original_stdout.write(text)
            self.logger._original_stdout.flush()
            return len(text)

    def flush(self):
        return None


@dataclass
class Logger:
    """A simple logger with colored output and formatting options"""

    def __init__(self, log_level: LogLevel = LogLevel.DEFAULT):
        self._log_level = log_level
        self._is_clean = False

        # Store original stdout and stderr
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr

        # Create and set up the logger stream
        self._logger_stream = LoggerStream(self)

        # Redirect stdout and stderr
        sys.stdout = self._logger_stream
        sys.stderr = self._logger_stream

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

    def cleanup(self) -> None:
        """Clean up the logger and restore original stdout/stderr"""
        if not self._is_clean:
            # Restore original stdout and stderr
            sys.stdout = self._original_stdout
            sys.stderr = self._original_stderr
            self._is_clean = True

    def __del__(self):
        # Call cleanup for safety
        self.cleanup()

    def set_log_level(self, level: LogLevel) -> None:
        """Set the log level for the logger

        Args:
            level: The log level to set (NONE, DEFAULT, or DEBUG)
        """
        # Clear the buffer when log level changes
        self._logger_stream.buffer = []
        self._log_level = level

    def print(self, prefix: str | None = None, message: str | None = None, payload: Any | None = None, color: Color | None = None, newline: bool = True, replace_last_line: bool = False, debug: bool = False) -> None:
        """Print a message with optional prefix, payload, and color

        Args:
            prefix: Optional prefix to prepend to the message
            message: Optional message to print
            payload: Optional payload to print after the message
            color: Optional color to use for the output
            newline: Whether to add a newline at the end
            replace_last_line: Whether to replace the last line of output
            debug: Whether this is a debug message (only shown in DEBUG level)
        """
        # Skip if log level is NONE
        if self._log_level == LogLevel.NONE:
            return

        # Skip debug messages if not in DEBUG level
        if debug and self._log_level != LogLevel.DEBUG:
            return

        output = [" ◉ UIN "]

        if prefix:
            output.append(f"[{prefix}]")

        if message:
            output.append(message)

        if payload is not None:
            output.append(str(payload))

        text = " ".join(output)

        if color:
            text = f"{color.value}{text}{Color.RESET.value}"

        if replace_last_line:
            # Move cursor up one line and clear the line
            self._original_stdout.write("\033[F\033[K")

        # Use original stdout to avoid recursion
        self._original_stdout.write(text + ("\n" if newline else ""))
        self._original_stdout.flush()

    def art(self, name: str, color: Color | None = None) -> None:
        """Print ASCII art with optional color

        Args:
            name: Name of the art to print
            color: Optional color to use for the art
        """
        # Skip if log level is NONE
        if self._log_level == LogLevel.NONE:
            return

        # Add your ASCII art here
        art_map = {
            "separator": "=" * 80,
            "star": "*" * 80,
            "dash": "-" * 80,
            "dot": "." * 80,
        }

        art = art_map.get(name, name)
        if color:
            art = f"{color.value}{art}{Color.RESET.value}"

        # Use original stdout to avoid recursion
        self._original_stdout.write(art + "\n")
        self._original_stdout.flush()

    def separator(self, prefix: str | None = None, message: str | None = None, color: Color | None = None) -> None:
        """Print a separator line with optional prefix and message

        Args:
            prefix: Optional prefix to prepend to the message
            message: Optional message to print in the separator
            color: Optional color to use for the separator
        """
        # Skip if log level is NONE
        if self._log_level == LogLevel.NONE:
            return

        self.art("separator", color)
        if message:
            self.print(prefix, message, color=color)
            self.art("separator", color)
        # Use original stdout to avoid recursion
        self._original_stdout.write("\n")
        self._original_stdout.flush()
