#!/usr/bin/python
import json
import settings
import pymongo
from bson import ObjectId
from Logger import Logger
from database import MongoDB

DATABASE = settings.database
COLLECTION = settings.collection

# Create an instance of logger class
logger = Logger()


class Media(dict):
    """
    A Media model that creates movie/show type document on mongodb
    """
    def __init__(self):
        """ Class instructor """
        pass

    def store(self):
        """ A function in this class to store a media, a movie or a show into the database """
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
    def retrieveAll(key, value, limit, offset):
        """ A function to retrieve all media, movies or shows, using an attribute of the media such as type For the
        attribute of a media, a key and its value needs to be defined, like 'release year' as key and '2013'
        as its value."""
        client = MongoDB.setupConnection()
        try:
            db = client[DATABASE]
            logger.Info("Retrieved database: ", str(db))
            collection = db[COLLECTION]
            logger.Info("Retrieved collection: ", str(collection))
            # Setting up pagination based on limit and offset
            starting = collection.find({key: value}).sort('_id', pymongo.ASCENDING)
            L_id = starting[offset]['_id']
            medias = collection.find({"$and": [{'_id': {"$gte": L_id}}, {key: value}]}).sort('_id', pymongo.ASCENDING).limit(limit)
            result = []
            for media in medias:
                result.append(JSONEncoder().encode(media))

            return result

        except Exception as error:
            logger.Error("Error in Media class, retrieve function: ", str(error))
        finally:
            MongoDB.closeConnection(client)

    @staticmethod
    def retrieve(_id, key, value):
        """ A function to retrieve a media, a movie or a show, using the media id or an attribute of the media or both
        , id and an attribute. For the attribute of a media, a key and its value needs to be defined, like
        'release year' as key and '2013' as its value."""
        client = MongoDB.setupConnection()
        try:
            db = client[DATABASE]
            logger.Info("Retrieved database: ", str(db))
            collection = db[COLLECTION]
            logger.Info("Retrieved collection: ", str(collection))
            if _id is None:
                medias = collection.find({key: value}).sort('_id', pymongo.ASCENDING)
                result = []
                for film in medias:
                    # logger.Info("Retrieved media: ", str(JSONEncoder().encode(film)))
                    result.append(film)

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
                media = collection.find_one({"_id": ObjectId(_id)})
                return JSONEncoder().encode(media)

            if (_id is not None) and (key is not None) and (value is not None):
                media = collection.find_one({"$and": [{"_id": ObjectId(_id)}, {key: value}]})
                return JSONEncoder().encode(media)

        except Exception as error:
            logger.Error("Error in Media class, retrieve function: ", str(error))
        finally:
            MongoDB.closeConnection(client)

    @staticmethod
    def reload(_id, key, value):
        """ A function to update a media based on its id. Attribute of the media as key and value of the attribute as
         value will be passed to this function as its arguments as well as media id."""
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
        """ A function for removing a media from the database using its id."""
        client = MongoDB.setupConnection()
        db = client[DATABASE]
        collection = db[COLLECTION]
        try:
            if _id:
                return collection.remove({"_id": ObjectId(_id)})
        except Exception as error:
            logger.Error("Error in Media class, remove function: ", str(error))
        finally:
            MongoDB.closeConnection(client)

    @staticmethod
    def testMoviesDB():
        """ This test function is created to test the Media class for movie documents in the database independently
        and find possible error and bugs in this class. It can be called by test.py python file which can be
        run separately."""

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
        """ This test function is created to test the Media class for show documents in the database independently
                and find possible error and bugs in this class. It can be called by test.py python file which can be
                run separately."""

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
    """ This class is created for converting the Mongodb document objects to json objects. """
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
