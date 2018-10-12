#!/usr/bin/python
import json
import settings
from bson import ObjectId
from Logger import Logger
from database import MongoDB

DATABASE = settings.database
COLLECTION = settings.collection

logger = Logger()


class Media(dict):
    """
    A Media model that creates movie/show type document on mongodb
    """

    def __init__(self, dict):
        super().__init__(dict)

    __getattr__ = dict.__getitem__
    __delattr__ = dict.__delitem__
    __setattr__ = dict.__setitem__

    def store(self):
        client = MongoDB.setupConnection()
        try:
            db = client[DATABASE]
            collection = db[COLLECTION]
            return collection.insert_one(self).inserted_id
        except Exception as error:
            logger.Error("Error in Media class, store function: ", str(error))
        finally:
            MongoDB.closeConnection(client)

    @staticmethod
    def retrieve(_id, key, value):
        client = MongoDB.setupConnection()
        try:
            db = client[DATABASE]
            collection = db[COLLECTION]
            if _id is None:
                movies = collection.find({key: value})
                result = []
                for movie in movies:
                    result.append(movie)

                if len(result) == 1:
                    return JSONEncoder().encode(result[0])
                elif len(result) > 1:
                    ms = []
                    for r in result:
                        ms.append(JSONEncoder().encode(r))
                    return ms
                else:
                    return []

            if key is None and value is None:
                m = collection.find_one({"_id": ObjectId(_id)})
                return JSONEncoder().encode(m)

            if (_id is not None) and (key is not None) and (value is not None):
                m = collection.find_one({"$and": [{"_id": ObjectId(_id)}, {key: value}]})
                return JSONEncoder().encode(m)

        except Exception as error:
            logger.Error("Error in Media class, retrieve function: ", str(error))
        finally:
            MongoDB.closeConnection(client)

    @staticmethod
    def reload(_id, key, value):
        global movie
        client = MongoDB.setupConnection()
        db = client[DATABASE]
        collection = db[COLLECTION]
        try:
            if _id:
                movie = collection.update_one({
                    '_id': _id
                }, {
                    '$set': {
                        key: value
                    }
                }, upsert=True)  # To avoid inserting the same document more than once
            return movie
        except Exception as error:
            logger.Error("Error in Media class, reload function: ", str(error))
        finally:
            MongoDB.closeConnection(client)

    @staticmethod
    def remove(_id):
        client = MongoDB.setupConnection()
        db = client[DATABASE]
        collection = db[COLLECTION]
        if _id:
            return collection.remove({"_id": ObjectId(_id)})
        MongoDB.closeConnection(client)

    @staticmethod
    def testMoviesDB():
        m = {
            "media type": "movie",
            "title": "test_movie",
            "release year": "2020",
            "duration": "0 min",
            "genre": "Documentary",
            "synopsis": "test_movie description"
        }

        test_movie = Media(m)
        logger.Info("Creating new media model with this movie: ", m)
        id = Media.store(test_movie)
        logger.Info("This movie object was just stored in the document: ", id)

        retrievedMovie = Media.retrieve(_id=id, key=None, value=None)
        logger.Info("Trying to retrieve movie object with this id: ", id)
        logger.Info("retrieved movie object: ", retrievedMovie)

        logger.Info("Updating movie item with id: ", id)
        updatedMovie = Media.reload(_id=id, key='duration', value='100 min')
        logger.Info("Update result: ", updatedMovie)

        # Get all the media records where the type is "movie"
        movies = Media.retrieve(_id=None, key='media type', value='movie')
        logger.Info("Retrieve movies by media type: ", movies)

        movie_2 = Media.retrieve(_id="5bbd68b960e7e317c45e21a3", key="media type", value='movie')
        logger.Info("Retrieve a movie by id and media type: ", movie_2)

    @staticmethod
    def testShowsDB():
        s = {
            "media type": "show",
            "title": "test_show",
            "release year": "2020",
            "duration": "0 min",
            "genre": "Animation",
            "episodes": "0",
            "synopsis": "test_show description"
        }

        test_show = Media(s)
        logger.Info("Creating new media model with this show: ", s)
        id = Media.store(test_show)
        logger.Info("This show object was just stored in the document: ", id)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
