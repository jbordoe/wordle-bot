import random
import unittest
from unittest.mock import Mock, patch

from lib.display.wordle_result_themer import WordleResultThemer
from lib.game.game_guess_result import GameGuessResult


class TestWordleResultThemer(unittest.TestCase):
    def setUp(self):
        random.seed(0)
        self.mock_result = Mock(spec=GameGuessResult)
        self.mock_result.text = "⬛🟨🟩⬛🟨"

    def test_map_result_default_theme(self):
        theme = "default"
        result_text = WordleResultThemer.map_result(self.mock_result, theme)
        self.assertEqual(result_text, "⬛🟨🟩⬛🟨")

    def test_map_result_specific_theme(self):
        theme = "hearts"
        result_text = WordleResultThemer.map_result(self.mock_result, theme)
        self.assertEqual(result_text, "🖤💛💚🖤💛")

    def test_map_result_random_theme(self):
        theme = "random"
        call_count = 0
        original_choice = random.choice
        # mock the first call to random.choice to return a theme
        # subsequent calls should behave normally
        def side_effect_func(seq):
            nonlocal call_count
            call_count += 1
            return "emoji" if call_count == 1 else original_choice(seq)

        with patch("random.choice", side_effect=side_effect_func):
            result_text = WordleResultThemer.map_result(self.mock_result, theme)

            self.assertEqual(result_text, "☹️😐🙂☹️😐")

    def test_map_result_shuffle_theme(self):
        theme = "shuffle"
        # For shuffle, we just ensure it returns a string and doesn't crash
        result_text = WordleResultThemer.map_result(self.mock_result, theme)
        self.assertIsInstance(result_text, str)
        self.assertEqual(len(result_text), len(self.mock_result.text))

if __name__ == '__main__':
    unittest.main()
