from typing import List, Optional, Set

from lib.game.game_constants import GameConstants
from lib.game.game_guess_letter import GameGuessLetter
from lib.game.game_guess_result import GameGuessResult


class PlayerKnowledge:
    """
    Encapsulates the state of knowledge a player has about the current game.
    This includes placed letters, present letters, and absent letters.
    """

    def __init__(self, word_length: int):
        self.word_length: int = word_length
        self.placed: List[Optional[str]] = [None] * word_length
        self.present: Set[str] = set()
        self.filter: Set[str] = set()
        self.excludes: List[Set[str]] = [set() for _ in range(word_length)]
        self.history: List[GameGuessResult] = []
        self.letters = [
            GameGuessLetter("", GameConstants.LETTER_STATE_INIT)
            for _ in range(word_length)
        ]

    def update_state(self, result: GameGuessResult) -> None:
        """
        Updates the player's knowledge based on the result of a guess.
        """
        self.history.append(result)
        self.letters = result.letters

        guess = result.guess
        seen = set()
        for i, letter_obj in enumerate(result.letters):
            letter = letter_obj.value

            if letter_obj.is_absent():
                if letter not in seen:
                    # If the letter is not present, it can't be placed.
                    self.filter.add(letter)
                continue
            if letter_obj.is_present():
                self.excludes[i].add(letter)  # We know this letter isn't placed here
                self.present.add(letter)
                self.filter.discard(letter)
            elif letter_obj.is_placed():
                self.placed[i] = letter
                self.filter.discard(letter)
                # A letter can be both placed and present
                # (e.g., guess "SASSY" for "BASIC")
                # If we know it only appears once, remove it from present set.
                if guess.count(letter) == 1:
                    self.present.discard(letter)
            else:
                raise ValueError(f"Invalid letter state: {letter_obj}")

            seen.add(letter)

    def previous_guesses(self) -> List[str]:
        return [result.guess for result in self.history if result.guess]
