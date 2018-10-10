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
    def getMovieData(title):
        try:
            url = 'http://www.omdbapi.com/?apikey=' + apikey + '&t=' + title
            r = requests.get(url)
            content = r.json()
            if content['Title'] != 'Title':
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

        except Exception as error:
            logger.Error("Error in getMovieData function: ", str(error))

    @staticmethod
    def getMoviesList():
        movies_list = []
        try:
            with open('./data/movieList.csv', newline='') as f:
                reader = csv.reader(f)
                for row in reader:
                    movies_list.append(row[0])
        except IOError as error:
            logger.Error("Error in getMoviesList function: ", str(error))

        return movies_list
