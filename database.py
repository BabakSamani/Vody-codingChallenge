#!/usr/bin/python
import settings
from Logger import Logger
from pymongo import MongoClient


MONGO_URL = 'mongodb://' + settings.host + ':' + settings.port + '/'
logger = Logger()


class MongoDB(object):
    def __init__(self):
        pass

    @staticmethod
    def setupConnection():
        try:
            client = MongoClient(MONGO_URL)
            message = 'Setting up the connection...'
            logger.Info("Database, MongoDB class: ", message)
            return client
        except Exception as error:
            logger.Error("Error in MongoDB,setupConnection: ", str(error))

    @staticmethod
    def closeConnection(client):
        try:
            message = 'Closing the connection...'
            logger.Info("Database, MongoDB class: ", message)
            client.close()
            return
        except Exception as error:
            logger.Error("Error in MongoDB,closeConnection: ", str(error))
