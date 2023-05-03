"""
    This module provides the default settings of the
    package test
"""

from importlib import metadata
from pathlib import Path


package = metadata.metadata('centopy')

name = package['name']
version = package['version']
author = package['author']
author_email = package['author-email']
summary = package['summary']

TITLE = name
DELIMITER = len(TITLE)*"="
HEADER = f"""
{DELIMITER}
{TITLE}
Version: {version}
Description: {summary }
Authors: {author}
{DELIMITER}
"""

CONFIG_LOG = {
    "version": 1,
    "formatters": {
        "client": {
            "format": "%(levelname)s: %(message)s"
        },
        "standard": {
            "format": "%(levelname)s - function: (%(name)s at %(funcName)s line %(lineno)d): %(message)s"
        },
        "file": {
            "format": "%(levelname)s - function: (%(name)s at %(funcName)s line %(lineno)d): %(message)s",
            "datefmt": "%y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "client": {
            "class": "logging.StreamHandler",
            "formatter": "client",
            "level": "INFO"
        },
        "standard": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "DEBUG"
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "file",
            "level": "DEBUG",
            "filename": "report.log",
            "encoding": "utf8"
        }
    },
    "root": {
        "handlers": [
            "standard"
        ],
        "level": "DEBUG"
    },
    "loggers": {
        "client": {
            "handlers": [
                "client"
            ],
            "level": "DEBUG",
            "propagate": False
        },
        "standard": {
            "handlers": [
                "standard"
            ],
            "level": "DEBUG",
            "propagate": False
        },
        "report": {
            "handlers": [
                "file"
            ],
            "level": "DEBUG",
            "propagate": False
        }
    }
}
