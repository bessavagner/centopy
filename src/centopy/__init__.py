"""
    Package centopy

    <Write the package's description here>
"""

import logging
from logging import NullHandler
from logging.config import dictConfig
from importlib.metadata import version

from settings import CONFIG_LOG

from .core import *  # The core module is the packages's API
from . import base
from . import utils

dictConfig(CONFIG_LOG)

# Set default logging handler to avoid \"No handler found\" warnings.
logging.getLogger(__name__).addHandler(NullHandler())

__version__ = version("centopy")
