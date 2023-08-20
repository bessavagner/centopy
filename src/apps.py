"""
    Package centopy

    This can be an sample app using the package
    or the app itself to feed the __main__ and gui
    modules.
"""

import logging
from logging.config import dictConfig

from centopy import CONFIG_LOG
from centopy import FilesManager

dictConfig(CONFIG_LOG)

logger = logging.getLogger('client')
report = logging.getLogger('report')

class Files:
    def __init__(self, *args, **kwargs):
        self.manager = FilesManager(*args, **kwargs)
    def show(self,):
        print(self.manager)
    def run(self, command, *args, **kwargs):
        action = getattr(self.manager, command)
        result = action(*args, **kwargs)
        return result
