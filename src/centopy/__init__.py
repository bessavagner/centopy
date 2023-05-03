"""
    Package centopy

    <Write the package's description here>
"""

import logging
from logging import NullHandler

from settings import *

from .core import *  # The core module is the packages's API
from . import base
from . import data
from . import utils

# Set default logging handler to avoid \"No handler found\" warnings.
logging.getLogger(__name__).addHandler(NullHandler())
