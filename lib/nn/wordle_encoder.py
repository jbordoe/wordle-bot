from typing import Dict, List, Tuple

from lib.game.game_guess_letter import GameGuessLetter


class WordleEncoder:
    """
    Encodes Wordle game states and target words into formats
    suitable for the neural network.
    """
    NUM_LETTERS: int = 26
    STATE_TO_IDX: Dict[str, int] = {'UNKNOWN': 0, 'PRESENT': 1, 'PLACED': 2}
    PAD_IDX: int = 26  # For '_' character in input
    VOCAB_SIZE: int = NUM_LETTERS
    SEQ_LEN: int = 5

    @staticmethod
    def encode_game_state(state: str) -> List[Tuple[int, int]]:
        """
        Encodes a Wordle game state string into a list
        of (letter_idx, state_idx) tuples.

        Parameters:
            state (str): The game state string, e.g., "eE_S_".
                         Lowercase for present, uppercase for placed, '_' for unknown.

        Returns:
            List[Tuple[int, int]]:
                A list of tuples, where each tuple contains:
                - letter_idx (int): 0-25 for A-Z, 26 for '_'.
                - state_idx (int): 0 = UNKNOWN, 1 = PRESENT, 2 = PLACED.
        """
        encoded = []
        for ch in state:
            if ch == '_':
                letter_idx = WordleEncoder.PAD_IDX
                state_idx = WordleEncoder.STATE_TO_IDX['UNKNOWN']
            elif ch.islower():
                letter_idx = ord(ch.upper()) - ord('A')
                state_idx = WordleEncoder.STATE_TO_IDX['PRESENT']
            else:
                letter_idx = ord(ch) - ord('A')
                state_idx = WordleEncoder.STATE_TO_IDX['PLACED']
            encoded.append((letter_idx, state_idx))
        return encoded

    @staticmethod
    def encode_result_letters_as_str(letters: List[GameGuessLetter]) -> str:
        """
        Encodes a list of GameGuessLetter into a string of [A-Za-z_] characters.

        Args:
            letters (List[GameGuessLetter])
        Returns:
            str: The encoded string.
            Example: "_A_eL" where lowercase is present, upcase is placed, _ is unknown
        """
        gamestring = ''
        for letter in letters:
            if letter.is_present():
                gamestring += letter.value.lower()
            elif letter.is_placed():
                gamestring += letter.value.upper()
            else:
                gamestring += '_'
        return gamestring

    @staticmethod
    def encode_label(word: str) -> List[int]:
        """
        Encodes a target word into a list of letter indices (0-25 for A-Z).

        Args:
            word (str): The target word, e.g., "EXECS".

        Returns:
            List[int]: A list of integer indices representing each letter in the word.
        """
        return [ord(c.upper()) - ord('A') for c in word]
