#!/usr/bin/python
import csv
import settings
import requests
from Logger import Logger

logger = Logger()
apikey = settings.api


class Data(object):
    def __init__(self):
        pass

    @staticmethod
    def getMediaData(media_type, title):
        try:
            url = 'http://www.omdbapi.com/?apikey=' + apikey + '&t=' + title
            r = requests.get(url)
            content = r.json()
            if content['Title'] != 'Title':
                if media_type == 'movie':
                    movie = {
                        'media type': 'movie',
                        'title': content['Title'],
                        'release year': content['Year'],
                        'duration': content['Runtime'],
                        'genre': content['Genre'],
                        'synopsis': content['Plot']
                    }

                    logger.Info("Movie:", movie)
                    return movie
                if media_type == 'show':
                    show = {
                        'media type': 'show',
                        'title': content['Title'],
                        'release year': content['Year'],
                        'duration': content['Runtime'],
                        'genre': content['Genre'],
                        'episodes': content['totalSeasons'],
                        'synopsis': content['Plot']
                    }

                    logger.Info("Show:", show)
                    return show

        except Exception as error:
            logger.Error("Error in getMediaData function: ", str(error))

    @staticmethod
    def getMoviesList():
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
        apikey = '9eca5109'
        media_list = ["The L Word", "Midnight Texas", "The Twilight Zone", "Ben 10",
                      "Marvel's Runaways", "Everwood", "X-Men", "The Exorcist", "Dollhouse",
                      "Don't Trust the B---- in Apartment 23", "Full Metal Panic!"]

        for title in media_list:
            url = 'http://www.omdbapi.com/?apikey=' + apikey + '&t=' + title
            r = requests.get(url)
            content = r.json()
            logger.Info("Received media:", content)
