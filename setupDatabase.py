#!/usr/bin/python
from dataFile import Data
from Models import Media


def setupDatabase():
    movies = Data.getMoviesList()

    # Setting up the database
    for i in range(1, len(movies)):
        m = Data.getMovieData(movies[i])
        try:
            movie = Media(m)
            Media.store(movie)
        except Exception as error:
            print(error)


def main():
    setupDatabase()


if __name__ == "__main__":
    main()
