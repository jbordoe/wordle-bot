from lib.game.game_interface import GameInterface


class PlayerKnowledge:
    """
    Encapsulates the state of knowledge a player has about the current game.
    This includes placed letters, present letters, and absent letters.
    """

    def __init__(self, word_length):
        self.word_length = word_length
        self.placed = [None for _ in range(word_length)]
        self.present = set()
        self.filter = set()
        self.excludes = [set() for _ in range(word_length)]
        self.history = []

    def update_state(self, result) -> None:
        """
        Updates the player's knowledge based on the result of a guess.
        """
        self.history.append(result)

        letters = result.letters
        guess = result.guess
        seen = set()
        for i, pair in enumerate(letters):
            letter, l_state = pair
            if l_state == GameInterface.LETTER_STATE_ABSENT:
                if letter not in seen:
                    # If the letter is not present, it can't be placed.
                    self.filter.add(letter)
                continue
            if l_state == GameInterface.LETTER_STATE_PRESENT:
                self.excludes[i].add(letter)  # We know this letter isn't placed here
                self.present.add(letter)
                self.filter.discard(letter)
            elif l_state == GameInterface.LETTER_STATE_PLACED:
                self.placed[i] = letter
                self.filter.discard(letter)
                # A letter can be both placed and present
                # (e.g., guess "SASSY" for "BASIC")
                # If we know it only appears once, remove it from present set.
                if guess.count(letter) == 1:
                    self.present.discard(letter)
            else:
                raise ValueError(f"Invalid letter state: {pair}")

            seen.add(guess[i])
