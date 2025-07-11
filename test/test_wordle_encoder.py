import unittest

from lib.game.game_constants import GameConstants
from lib.game.game_guess_letter import GameGuessLetter
from lib.nn.wordle_guesser_model import WordleEncoder


class TestWordleEncoder(unittest.TestCase):

    def test_encode_game_state(self):
        state = "aB_cD"
        expected = [
            (0, WordleEncoder.STATE_TO_IDX['PRESENT']),
            (1, WordleEncoder.STATE_TO_IDX['PLACED']),
            (WordleEncoder.PAD_IDX, WordleEncoder.STATE_TO_IDX['UNKNOWN']),
            (2, WordleEncoder.STATE_TO_IDX['PRESENT']),
            (3, WordleEncoder.STATE_TO_IDX['PLACED']),
        ]
        self.assertEqual(WordleEncoder.encode_game_state(state), expected)

    def test_encode_result_letters_as_str(self):
        letters = [
            GameGuessLetter("A", GameConstants.LETTER_STATE_PRESENT),
            GameGuessLetter("P", GameConstants.LETTER_STATE_PLACED),
            GameGuessLetter("P", GameConstants.LETTER_STATE_ABSENT),
            GameGuessLetter("L", GameConstants.LETTER_STATE_PLACED),
            GameGuessLetter("E", GameConstants.LETTER_STATE_PLACED)
        ]
        expected = "aP_LE"
        self.assertEqual(
            WordleEncoder.encode_result_letters_as_str(letters),
            expected
        )

    def test_encode_label(self):
        word = "APPLE"
        expected = [0, 15, 15, 11, 4]
        self.assertEqual(WordleEncoder.encode_label(word), expected)

    def test_encode_label_lowercase(self):
        word = "apple"
        expected = [0, 15, 15, 11, 4]
        self.assertEqual(WordleEncoder.encode_label(word), expected)

if __name__ == '__main__':
    unittest.main()
