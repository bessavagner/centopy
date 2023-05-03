"""
    Package centopy

    This can be an sample app using the package
    or the app itself to feed the __main__ and gui
    modules.
"""

import logging
from logging.config import dictConfig

from centopy import CONFIG_LOG
from centopy import NameYourClass

dictConfig(CONFIG_LOG)

logger = logging.getLogger('client')
report = logging.getLogger('report')

class MyApp:
    def __init__(self, *args, **kwargs):
        self.attribute = NameYourClass(*args, **kwargs)
    def show(self,):
        print(self.attribute.action)
    def run(self,):
        logger.info('Running application')
        if self.attribute.action is None:
            logger.warning('No action specified')
        return self.attribute.action
