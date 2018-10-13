#!/usr/bin/python
import csv
import settings
import requests
from Logger import Logger

logger = Logger()
API_URL = [settings.api_url_1, settings.api_url_2]


class Data(object):
    def __init__(self):
        pass

    num_of_calls = 1

    @staticmethod
    def getMediaData(media_type, title):
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
                        'year': content['Year'],
                        'released': content['Released'],
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
        media_list = ["The L Word", "Midnight Texas", "The Twilight Zone", "Ben 10",
                      "Marvel's Runaways", "Everwood", "X-Men", "The Exorcist", "Dollhouse",
                      "Don't Trust the B---- in Apartment 23", "Full Metal Panic!"]

        for title in media_list:
            url = API_URL[1] + title
            r = requests.get(url)
            content = r.json()
            logger.Info("Received media:", content)
