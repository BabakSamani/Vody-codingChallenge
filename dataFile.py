#!/usr/bin/python
import csv
import settings
import requests
from Logger import Logger

logger = Logger()
# Get API url from settings.py and .env file
API_URL = [settings.api_url_1, settings.api_url_2]


class Data(object):
    def __init__(self):
        pass

    num_of_calls = 1

    @staticmethod
    def getMediaData(media_type, title):
        """
        This function gets data for a movie or show from an api and returns a movie or show JSON object to store
        on collection of documents on a Mongodb type database.
        :returns: a JSON object
        """
        if Data.num_of_calls <= 1000:
            api_url = API_URL[0]
            Data.num_of_calls += 1
        else:
            api_url = API_URL[1]
            Data.num_of_calls += 1
        try:
            url = api_url + title
            r = requests.get(url)
            content = r.json()
            # if api returns a valid info for a requested media
            if content['Title'] != 'Title':
                # Create JSON object of movie type
                if media_type == 'movie':
                    movie = {
                        'media type': 'movie',
                        'title': content['Title'],
                        'release year': content['Year'],
                        'duration': content['Runtime'],
                        'genre': content['Genre'],
                        'synopsis': content['Plot']
                    }
                    # A logger to check the result
                    logger.Info("Movie:", movie)
                    return movie
                # Create JSON object of show type
                if media_type == 'show':
                    show = {
                        'media type': 'show',
                        'title': content['Title'],
                        'year': content['Year'],
                        'released': content['Released'],
                        'duration': content['Runtime'],
                        'genre': content['Genre'],
                        'episodes': content['totalSeasons'],
                        'synopsis': content['Plot']
                    }
                    # A logger to check the result
                    logger.Info("Show:", show)
                    return show

        except Exception as error:
            logger.Error("Error in getMediaData function: ", str(error))

    @staticmethod
    def getMoviesList():
        """
        A function to create a list of movies from a cvs file. The csv file is located in the /data directory.
        This function returns a list of movies in an array.
        :returns: an array
        """
        movies_list = []
        try:
            with open('./data/movieList.csv', 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    movies_list.append(row[0])
        except IOError as error:
            logger.Error("Error in getMoviesList function: ", str(error))

        return movies_list

    @staticmethod
    def getShowsList():
        """
        A function to create a list of shows from a cvs file. The csv file is located in the /data directory.
        This function returns a list of shows in an array.
        :returns: an array
        """
        shows_list = []
        try:
            with open('./data/TVshowList.csv', 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    shows_list.append(row[0])
        except IOError as error:
            logger.Error("Error in getShowsList function: ", str(error))

        return shows_list

    @staticmethod
    def test_getDataFromAPI():
        """
        A test function in this class for testing the api and see whether we can get data from api. This test can be
        called from test.py python script.
        :return: none
        """
        media_list = ["The L Word", "Midnight Texas", "The Twilight Zone", "Ben 10",
                      "Marvel's Runaways", "Everwood", "X-Men", "The Exorcist", "Dollhouse",
                      "Don't Trust the B---- in Apartment 23", "Full Metal Panic!"]

        for title in media_list:
            url = API_URL[1] + title
            r = requests.get(url)
            content = r.json()
            logger.Info("Received media:", content)
