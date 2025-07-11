from lib.game.game_constants import GameConstants


class GameGuessLetter:
    def __init__(self, value: str, state: int):
        self.value = value
        self.state = state

    def is_present(self) -> bool:
        return self.state == GameConstants.LETTER_STATE_PRESENT

    def is_placed(self) -> bool:
        return self.state == GameConstants.LETTER_STATE_PLACED

    def is_absent(self) -> bool:
        return self.state == GameConstants.LETTER_STATE_ABSENT

    def __eq__(self, other):
        if not isinstance(other, GameGuessLetter):
            return False
        return self.value == other.value and self.state == other.state

    def __repr__(self):
        return f"GameGuessLetter(value='{self.value}', state={self.state})"
