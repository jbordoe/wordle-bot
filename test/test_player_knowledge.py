import unittest
from unittest.mock import MagicMock

from lib.game.game_constants import GameConstants
from lib.game.game_guess_letter import GameGuessLetter
from lib.player.player_knowledge import PlayerKnowledge


class TestPlayerKnowledge(unittest.TestCase):
    def setUp(self):
        """
        Set up a new PlayerKnowledge instance for each test.
        """
        self.knowledge = PlayerKnowledge(word_length=5)

    def test_initialization(self):
        """
        Tests that PlayerKnowledge is instantiated with the correct empty state.
        """
        self.assertEqual(self.knowledge.word_length, 5)
        self.assertEqual(self.knowledge.placed, [None, None, None, None, None])
        self.assertEqual(self.knowledge.present, set())
        self.assertEqual(self.knowledge.filter, set())
        self.assertEqual(self.knowledge.excludes, [set(), set(), set(), set(), set()])

    def test_update_state_simple(self):
        """
        Tests a straightforward update with absent, present, and placed letters.
        """
        mock_result = MagicMock()
        mock_result.guess = "RAISE"
        mock_result.letters = [
            GameGuessLetter(value="R", state=GameConstants.LETTER_STATE_ABSENT),
            GameGuessLetter(value="A", state=GameConstants.LETTER_STATE_PLACED),
            GameGuessLetter(value="I", state=GameConstants.LETTER_STATE_PRESENT),
            GameGuessLetter(value="S", state=GameConstants.LETTER_STATE_ABSENT),
            GameGuessLetter(value="E", state=GameConstants.LETTER_STATE_PLACED),
        ]

        self.knowledge.update_state(mock_result)

        self.assertEqual(self.knowledge.placed, [None, "A", None, None, "E"])
        self.assertEqual(self.knowledge.present, {"I"})
        self.assertEqual(self.knowledge.filter, {"R", "S"})
        self.assertEqual(self.knowledge.excludes[2], {"I"})

    def test_update_state_with_duplicate_letters(self):
        """
        Tests an update where a guessed letter appears twice, but one is absent.
        Example: Guessing "APPLE" when the word is "PATCH". The first P is absent.
        """
        mock_result = MagicMock()
        mock_result.guess = "APPLE"
        mock_result.letters = [
            GameGuessLetter(value="A", state=GameConstants.LETTER_STATE_PRESENT),
            GameGuessLetter(value="P", state=GameConstants.LETTER_STATE_ABSENT),
            GameGuessLetter(value="P", state=GameConstants.LETTER_STATE_PLACED),
            GameGuessLetter(value="L", state=GameConstants.LETTER_STATE_ABSENT),
            GameGuessLetter(value="E", state=GameConstants.LETTER_STATE_PRESENT),
        ]

        self.knowledge.update_state(mock_result)

        self.assertEqual(self.knowledge.placed, [None, None, "P", None, None])
        self.assertEqual(self.knowledge.present, {"A", "E"})
        self.assertEqual(self.knowledge.filter, {"L"})  # P should not be in filter
        self.assertEqual(self.knowledge.excludes[0], {"A"})
        self.assertEqual(self.knowledge.excludes[4], {"E"})

    def test_update_state_placed_letter_also_present(self):
        """
        Tests an update where a letter is placed, but also appears elsewhere.
        Example: Guessing "SASSY" when the word is "BASIC". The first S is absent,
        the second is present, and the third is placed.
        """
        mock_result = MagicMock()
        mock_result.guess = "SASSY"
        mock_result.letters = [
            GameGuessLetter(value="S", state=GameConstants.LETTER_STATE_ABSENT),
            GameGuessLetter(value="A", state=GameConstants.LETTER_STATE_PRESENT),
            GameGuessLetter(value="S", state=GameConstants.LETTER_STATE_PRESENT),
            GameGuessLetter(value="S", state=GameConstants.LETTER_STATE_PLACED),
            GameGuessLetter(value="Y", state=GameConstants.LETTER_STATE_ABSENT),
        ]

        self.knowledge.update_state(mock_result)

        self.assertEqual(self.knowledge.placed, [None, None, None, "S", None])
        self.assertEqual(self.knowledge.present, {"A", "S"})
        self.assertEqual(self.knowledge.filter, {"Y"})  # First S is not added to filter
        self.assertEqual(self.knowledge.excludes[1], {"A"})
        self.assertEqual(self.knowledge.excludes[2], {"S"})

    def test_raises_on_invalid_letter_state(self):
        """
        Tests that an invalid letter state raises an exception.
        """
        mock_result = MagicMock()
        mock_result.guess = "APPLE"
        mock_result.letters = [
            GameGuessLetter(value="A", state=GameConstants.LETTER_STATE_PRESENT),
            GameGuessLetter(value="P", state=GameConstants.LETTER_STATE_ABSENT),
            GameGuessLetter(value="L", state=GameConstants.LETTER_STATE_ABSENT),
            GameGuessLetter(value="E", state="invalid"),
            GameGuessLetter(value="P", state=GameConstants.LETTER_STATE_PRESENT),
        ]
        with self.assertRaises(ValueError):
            self.knowledge.update_state(mock_result)

    def test_previous_guesses(self):
        """
        Tests that the previous guesses are correctly returned
        """
        mock_results = [
            MagicMock(guess="APPLE"),
            MagicMock(guess="SASSY"),
            MagicMock(guess="RAISE"),
        ]
        for result in mock_results:
            self.knowledge.update_state(result)

        self.assertEqual(
            self.knowledge.previous_guesses(),
            ["APPLE", "SASSY", "RAISE"]
        )

if __name__ == "__main__":
    unittest.main()
