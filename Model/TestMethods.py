import math
import os.path
import pathlib
from random import randint

import pandas as pd
import numpy as np

GuessTooLarge = 1
CorrectGuess = 0
GuessTooSmall = -1

'''
Return both a list of the least rated and most rated movies
'''


def getMovieRatingsThings() -> [list, list]:
    prefix = pathlib.Path(__file__).parent.resolve().__str__()
    df_ratings: pd.DataFrame = pd.read_csv(prefix + '/ratings.dat', sep="::",
                                           names=['user_id', 'movie_id', 'rating', 'timestamp']).drop('timestamp',
                                                                                                      1).pivot(
        index='movie_id',
        columns='user_id',
        values='rating'
    )
    df_movies: pd.DataFrame = pd.read_csv(prefix + '/movies.dat', sep="::", names=['movie_id', 'title', 'genre'],
                                          encoding='windows-1252')
    df_movie_dict = dict(zip(df_movies.movie_id, df_movies.title))

    df_ratings['null_count'] = df_ratings.isnull().sum(axis=1)
    df_lowest_rating = df_ratings.sort_values('null_count', ascending=False).drop('null_count', axis=1)
    df_highest_rating = df_ratings.sort_values('null_count', ascending=True).drop('null_count', axis=1)
    listOfLowestRatedMovies = []
    listOfHighestRatedMovies = []

    j = 0
    for i in df_lowest_rating.iterrows():
        listOfLowestRatedMovies.append(df_movie_dict[i[0]])
        j += 1
        if (j > 100):
            break

    j = 0
    for i in df_highest_rating.iterrows():
        listOfHighestRatedMovies.append(df_movie_dict[i[0]])
        j += 1
        if (j > 100):
            break

    return listOfLowestRatedMovies, listOfHighestRatedMovies


# @DeprecationWarning
def wrapMovies(gender, age, occupation, zipcode):
    list = [gender, age, occupation, zipcode]
    l = '0' + "::" + gender + "::" + age
    print(l)
    return l


if __name__ == "__main__":
    getMovieRatingsThings()
