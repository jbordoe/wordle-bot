import random
from lib.game_guess_result import GameGuessResult

class GameStateInterface:
    LETTER_STATE_PRESENT = 0
    LETTER_STATE_PLACED = 1

    def __init__(self):
        pass

    def update(self, guess) -> GameGuessResult:
        pass

    def quit(self):
        pass
