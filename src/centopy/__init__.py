"""
    Package centopy

    <Write the package's description here>
"""

import logging
from logging import NullHandler
from logging.config import dictConfig

from settings import *

from .core import *  # The core module is the packages's API
from . import base
from . import utils

dictConfig(CONFIG_LOG)

# Set default logging handler to avoid \"No handler found\" warnings.
logging.getLogger(__name__).addHandler(NullHandler())
