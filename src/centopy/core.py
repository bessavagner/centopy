"""
    Package "centopy"

    This module provides package's api
"""

import logging
from .base import BaseNameYourClass
from .utils import important_action

logger = logging.getLogger('standard')

class NameYourClass(BaseNameYourClass):
    def __init__(self, *args, **kwargs):
        logger.info('Object created!')
        self.action = important_action(*args, **kwargs)
