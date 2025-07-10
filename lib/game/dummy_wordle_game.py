import random

from lib.game.game_guess_result import GameGuessResult
from lib.game.game_interface import GameInterface


class DummyWordleGame(GameInterface):
    def __init__(self, wordlist=None):
        self.wordlist = wordlist
        self.word_length = len(wordlist[0])
        self.answer = random.sample(wordlist, 1)[0].upper()
        self.guesses = 0
        self.letter_counts = {
            letter: self.answer.count(letter) for letter in self.answer
        }

    def update(self, guess):
        letters = [None for _ in range(len(guess))]
        guess_letter_counts = {}
        for i, letter in enumerate(guess):
            if letter == self.answer[i]:
                letters[i] = (letter, self.LETTER_STATE_PLACED)
            elif (
                letter in self.answer
                and guess_letter_counts.get(letter, 0) < self.letter_counts[letter]
            ):
                letters[i] = (letter, self.LETTER_STATE_PRESENT)
            else:
                letters[i] = (letter, self.LETTER_STATE_ABSENT)
            guess_letter_counts[letter] = guess_letter_counts.get(letter, 0) + 1

        self.guesses += 1

        res = GameGuessResult(guess, letters=letters, correct=guess == self.answer)
        return res
