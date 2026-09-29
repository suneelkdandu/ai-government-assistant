import logging
import os
import sys


LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
).upper()


def get_logger(name):
    """
    Return a configured application logger.

    Logs are written to the terminal.
    No API keys, prompts or document text are logged.
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    valid_levels = {
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL"
    }

    level_name = (
        LOG_LEVEL
        if LOG_LEVEL in valid_levels
        else "INFO"
    )

    logger.setLevel(
        getattr(logging, level_name)
    )

    handler = logging.StreamHandler(
        sys.stderr
    )

    formatter = logging.Formatter(
        fmt=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    logger.propagate = False

    return logger
