from lib.game.game_constants import GameConstants
from lib.game.game_guess_result import GameGuessResult


class GameInterface:
    LETTER_STATE_PRESENT = GameConstants.LETTER_STATE_PRESENT
    LETTER_STATE_PLACED = GameConstants.LETTER_STATE_PLACED
    LETTER_STATE_ABSENT = GameConstants.LETTER_STATE_ABSENT

    def __init__(self):
        raise NotImplementedError

    def update(self, guess) -> GameGuessResult:
        raise NotImplementedError

    def undo(self):
        raise NotImplementedError

    def quit(self):
        raise NotImplementedError
