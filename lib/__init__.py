import logging
import os
from colorlog import ColoredFormatter

logger = logging.getLogger()

# Check if the logger already has handlers. This is to prevent adding handlers multiple times,
# which can happen if this module is imported more than once.
if not logger.handlers:
    logger.setLevel(os.environ.get("LOG_LEVEL", "INFO").upper())

    handler = logging.StreamHandler()
    formatter = ColoredFormatter(
        '%(log_color)s%(levelname)-8s%(reset)s %(log_color)s%(message)s',
        log_colors={
            'DEBUG':    'light_cyan',
            'INFO':     'light_green',
            'WARNING':  'light_yellow',
            'ERROR':    'light_red',
            'CRITICAL': 'light_red,bg_white',
        }
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)
