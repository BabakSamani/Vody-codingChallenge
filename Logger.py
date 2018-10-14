#!/usr/bin/python
import os
import json
import logging
import logging.config  # configuration and settings for this class


class Logger(object):
    def __init__(self):
        """ Setup logging configuration """
        default_path = 'logging.json'
        default_level = logging.INFO
        env_key = 'LOG_CFG'

        path = default_path
        value = os.getenv(env_key, None)
        if value:
            path = value
        if os.path.exists(path):
            with open(path, 'rt') as f:
                config = json.load(f)
                logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=default_level)

    @staticmethod
    def Info(class_name, msg):
        logger = logging.getLogger(class_name)
        logger.info(msg)

    @staticmethod
    def Debug(class_name, msg):
        logger = logging.getLogger(class_name)
        logger.debug(msg)

    @staticmethod
    def Warning(class_name, msg):
        logger = logging.getLogger(class_name)
        logger.warning(msg)

    @staticmethod
    def Error(class_name, msg):
        logger = logging.getLogger(class_name)
        logger.error(msg)
