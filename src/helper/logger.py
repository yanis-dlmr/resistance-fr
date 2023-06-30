import os

from dotenv import load_dotenv

import logging

from .formatter import *

__all__ = ['logger', 'log_lvl', 'console_handler', 'default_formatter']

# we load the env variables here so that we can use them in the logger
# because this file is imported in the main file first,
# we can't load the env variables in the main file
load_dotenv()
DEBUG = os.getenv('DEBUG', 'False').lower() in {'true', '1', 'yes'}

logger = logging.getLogger('me 🙂')
logger.setLevel(log_lvl := logging.DEBUG if DEBUG else logging.INFO)

# create console handler with a higher log level
console_handler = logging.StreamHandler()
console_handler.setLevel(log_lvl)
console_handler.setFormatter(default_formatter := UsefulFormatter())

logger.addHandler(console_handler)
