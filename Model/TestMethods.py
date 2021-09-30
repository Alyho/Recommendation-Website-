import math
from random import randint

GuessTooLarge = 1
CorrectGuess = 0
GuessTooSmall = -1


class NumberGuessing:

    def __init__(self, range=(0, 100)):
        self.num = randint(*range)
        self.tries = math.log2(self.num)

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
