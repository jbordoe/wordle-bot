import random
from lib.game.game_guess_result import GameGuessResult

class GameInterface:
    LETTER_STATE_PRESENT = 0
    LETTER_STATE_PLACED = 1

    def __init__(self):
        raise NotImplementedError

    def update(self, guess) -> GameGuessResult:
        raise NotImplementedError

    def undo(self):
        raise NotImplementedError

    def quit(self):
        raise NotImplementedError
