"""Load the logging configurations from a YAML file."""

import sys
import os
import logging
from logging.config import dictConfig
from pathlib import Path
import yaml
from functools import wraps

_here = Path(__file__).parent

LOG_FILE = os.getenv('BEACON_LOG', _here / "logger.yml")

def _find_logger_and_load():
    """Try to load `filename` as configuration file."""

    _logger = Path(LOG_FILE)

    if not _logger.exists():
        print(f"The file '{_logger}' does not exist", file=sys.stderr)
        return

    if _logger.suffix in ('.yaml', '.yml'):
        with open(_logger, 'r') as stream:
            dictConfig(yaml.safe_load(stream))
            return

    # Otherwise, fail
    print(f"Unsupported log format for {_logger}", file=sys.stderr)


def load_logger(func):
    '''Configuration decorator'''
    @wraps(func)
    def wrapper(*args, **kwargs):
        _find_logger_and_load()
        return func(*args, **kwargs)
    return wrapper