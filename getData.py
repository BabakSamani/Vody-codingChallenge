#!/usr/bin/python
import csv
import requests
from Logger import Logger
from database import MongoDB

logger = Logger()
__apikey = '9eca5109'


def getMovieData(title):
    try:
        url = 'http://www.omdbapi.com/?apikey=' + __apikey + '&t=' + title
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


# def insertIntoTable(table_name, data):
# def createTable(table_name):


def main():

    movies = getMoviesList()
    # collection = MongoDB.getCollection(database='Vody', collection='media')

    for i in range(1, len(movies)):
        movie = getMovieData(movies[i])
        MongoDB.insertData(movie)


if __name__ == "__main__":
    main()
