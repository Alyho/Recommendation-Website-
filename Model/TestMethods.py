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
    df_ratings: pd.DataFrame = pd.read_csv(  prefix+'/ratings.dat', sep="::",
                                           names=['user_id', 'movie_id', 'rating', 'timestamp']).drop('timestamp',
                                                                                                      1).pivot(
        index='movie_id',
        columns='user_id',
        values='rating'
    )
    df_movies: pd.DataFrame = pd.read_csv(prefix+'/movies.dat', sep="::", names=['movie_id', 'title', 'genre'],
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

def getRecommendedMovies(gender, age, occupation, zipcode):
    list = [gender, age, occupation, zipcode]
    return list 



class NumberGuessing:

    def __init__(self, value_range=(0, 100)):
        self.num = randint(*value_range)
        self.tries = int(math.log2(value_range[-1] - value_range[0])) + 1

    # Guess too large -> Your guess was larger than the real number
    # Guess too small -> Your guess was smaller than the real number
    def guess(self, guess: int):
        # If you used all your tries:
        if self.tries <= 0: return -999

        value = -1

        # How close is the guess?
        if guess > self.num:
            value = GuessTooLarge
        elif guess < self.num:
            value = GuessTooSmall
        else:
            value = CorrectGuess

        # One attempt
        if value != 0: self.tries -= 1

        # Return value
        return value

    def reset(self, value_range=(0, 100)):
        self.num = randint(*value_range)
        self.tries = int(math.log2(value_range[-1] - value_range[0])) + 1


if __name__ == "__main__":
    getMovieRatingsThings()
