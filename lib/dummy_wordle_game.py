import random
from lib.game_guess_result import GameGuessResult
from lib.game_state_interface import GameStateInterface

class DummyWordleGame(GameStateInterface):
    def __init__(self, wordlist=None):
        self.wordlist = wordlist
        self.word_length = len(wordlist[0])
        self.answer = random.sample(wordlist, 1)[0].upper()
        self.guesses = 0

    def update(self, guess):
        letters = [None for _ in range(len(guess))]
        for i, letter in enumerate(guess):
            if letter == self.answer[i]:
                letters[i] = (letter, self.LETTER_STATE_PLACED)
            elif letter in self.answer:
                letters[i] = (letter, self.LETTER_STATE_PRESENT)

        self.guesses += 1

        res = GameGuessResult(
            guess,
            letters=letters,
            correct=guess == self.answer
        )
        return res
