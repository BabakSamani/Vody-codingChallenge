#!/usr/bin/python
from dataFile import Data
from Models import Media
from Logger import Logger

logger = Logger()


def setupDatabase():
    # Get the list of movies and shows
    movies = Data.getMoviesList()
    shows = Data.getShowsList()

    # Setting up movies database
    for i in range(1, len(movies)):
        m = Data.getMediaData(media_type='movie', title=movies[i])
        try:
            movie = Media(m)
            Media.store(movie)
        except Exception as error:
            logger.Error("Error in setting up movies database: ", str(error))

    # Setting up shows database
    for i in range(1, len(shows)):
        s = Data.getMediaData(media_type='show', title=shows[i])
        try:
            show = Media(s)
            Media.store(show)
        except Exception as error:
            logger.Error("Error in setting up shows database: ", str(error))


def main():
    setupDatabase()


if __name__ == "__main__":
    main()
