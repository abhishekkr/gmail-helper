# -*- coding: utf-8 -*-
"""
Exposes a logging object by name 'logger' for default exposed log activities.
"""
import logging
import sys
from logging.handlers import TimedRotatingFileHandler

import _config_ as _cfg


FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")
LOG_FILE  = ""
try:
    logfilepath = os.environ['GMAIL_HELPER_LOGFILE']
    if len(logfilepath) > 0:
        LOG_FILE = logfilepath
except:
    print('no log file path provided via env "GMAIL_HELPER_LOGFILE", only console mode available')


def get_console_handler():
    """Returns console handler based on global configured formatter.

    Args: None
    """
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    """Returns file handler based on global configured LOG_FILE and FORMATTER.

    Args: None
    """
    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name):
    """Returns logger object with console and file handler attached.

    Args:
        logger_name: an id for logging object generated
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO) # default INFO mode for logging
    try:
        if _cfg.log_debug() == 'on':
            logger.setLevel(logging.DEBUG)
    except:
        print('default logging mode enabled, can turn on debug by env "GMAIL_HELPER_DEBUG=on"')
    logger.addHandler(get_console_handler())
    if len(LOG_FILE) > 0:
        logger.addHandler(get_file_handler())
    logger.propagate = False
    return logger


# default logger, to be used wherever imported
logger = get_logger('gmail-helper')
