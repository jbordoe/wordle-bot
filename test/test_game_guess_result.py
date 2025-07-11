import unittest

from lib.game.game_constants import GameConstants
from lib.game.game_guess_letter import GameGuessLetter
from lib.game.game_guess_result import GameGuessResult


class TestGameGuessResult(unittest.TestCase):
    def setUp(self):
        """
        Set up a sample GameGuessResult object for testing.
        """
        self.guess_word = "APPLE"
        self.letter_details = [
            ("A", GameConstants.LETTER_STATE_PLACED),
            ("P", GameConstants.LETTER_STATE_ABSENT),
            ("P", GameConstants.LETTER_STATE_PRESENT),
            ("L", GameConstants.LETTER_STATE_ABSENT),
            ("E", GameConstants.LETTER_STATE_PLACED),
        ]
        self.result_text = "Shareable result text"

        self.guess_result = GameGuessResult(
            guess=self.guess_word,
            letters=self.letter_details,
            correct=False,
            text=self.result_text,
        )

    def test_initialization_with_all_arguments(self):
        """
        Tests that all attributes are correctly assigned when provided.
        """
        self.assertEqual(self.guess_result.guess, self.guess_word)
        expected_letters = [
            GameGuessLetter(value="A", state=GameConstants.LETTER_STATE_PLACED),
            GameGuessLetter(value="P", state=GameConstants.LETTER_STATE_ABSENT),
            GameGuessLetter(value="P", state=GameConstants.LETTER_STATE_PRESENT),
            GameGuessLetter(value="L", state=GameConstants.LETTER_STATE_ABSENT),
            GameGuessLetter(value="E", state=GameConstants.LETTER_STATE_PLACED),
        ]
        self.assertEqual(self.guess_result.letters, expected_letters)
        self.assertFalse(self.guess_result.correct)
        self.assertEqual(self.guess_result.text, self.result_text)

    def test_initialization_with_defaults(self):
        """
        Tests that default values are used when optional arguments are omitted.
        """
        simple_result = GameGuessResult(guess="TESTS")

        self.assertEqual(simple_result.guess, "TESTS")
        expected_letters = [
            GameGuessLetter(value="", state=GameConstants.LETTER_STATE_INIT)
            for _ in range(5)
        ]
        self.assertEqual(simple_result.letters, expected_letters)
        self.assertFalse(simple_result.correct)
        self.assertEqual(simple_result.text, "")


if __name__ == "__main__":
    unittest.main()
