#!/usr/bin/python
import settings
from Logger import Logger
from pymongo import MongoClient


MONGO_URL = 'mongodb://' + settings.host + ':' + settings.port + '/'
logger = Logger()


class MongoDB(object):
    """
    This class is for making connection to the database or closing connection from the database.
    """
    def __init__(self):
        pass

    @staticmethod
    def setupConnection():
        """
        This function sets up a connection to a database on the Mongodb database.
        :return: connection tier to database
        """
        try:
            client = MongoClient(MONGO_URL)
            message = 'Setting up the connection...'
            logger.Info("Database, MongoDB class: ", message)
            return client
        except Exception as error:
            logger.Error("Error in MongoDB,setupConnection: ", str(error))

    @staticmethod
    def closeConnection(client):
        """
        This function closes a connection to a database on the Mongodb database.
        :return: none
        """
        try:
            message = 'Closing the connection...'
            logger.Info("Database, MongoDB class: ", message)
            client.close()
            return
        except Exception as error:
            logger.Error("Error in MongoDB,closeConnection: ", str(error))
