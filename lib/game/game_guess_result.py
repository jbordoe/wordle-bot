from typing import List, Optional, Tuple

from lib.game.game_constants import GameConstants
from lib.game.game_guess_letter import GameGuessLetter


class GameGuessResult:
    def __init__(
        self,
        guess: str,
        letters: Optional[List[Tuple[str, int]]] = None,
        correct: bool = False,
        text: str = "",
        valid: bool = True,
    ):
        """
        Represents the result of a guess

            Parameters:
                guess (str): The guessed word
                letters (List[Tuple[str, int]]): The guessed letters and their state
                correct (bool): Whether the guess was correct
                text (str): Any additional text to display
                valid (bool): Whether the guess is valid
        """
        self.guess = guess
        self.letters: List[GameGuessLetter] = []
        if letters:
            for letter_value, letter_state in letters:
                self.letters.append(GameGuessLetter(letter_value, letter_state))
        else:
            self.letters = [
                GameGuessLetter("", GameConstants.LETTER_STATE_INIT)
                for _ in range(len(guess))
            ]

        self.correct = correct
        self.text = text or ""
        self.valid = valid
