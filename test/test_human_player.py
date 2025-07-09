import unittest
from unittest.mock import patch, Mock
from lib.player.human_player import HumanPlayer

class TestHumanPlayer(unittest.TestCase):
    def test_initialization(self):
        HumanPlayer()

    @patch('lib.player.human_player.input')
    def test_guess_returns_valid_guess(self, mock_input):
        mock_input.return_value = "HELLO"
        player = HumanPlayer()
        game_state = Mock()
        game_state.wordlist = ["HELLO", "WORLD"]

        guess = player.guess(game_state)

        self.assertEqual(guess, "HELLO")

    @patch('lib.player.human_player.input')
    def test_guess_retried_until_valid_guess(self, mock_input):
        mock_input.side_effect = ["123", "FLORA", "HELLO"]
        player = HumanPlayer()
        game_state = Mock()
        game_state.wordlist = ["HELLO", "WORLD"]

        guess = player.guess(game_state)

        self.assertEqual(guess, "HELLO")
        mock_input.return_value = "WORLD"

    def test_update_state_does_nothing(self):
        HumanPlayer().update_state(None)

if __name__ == '__main__':
    unittest.main()

