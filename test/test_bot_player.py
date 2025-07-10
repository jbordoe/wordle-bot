import unittest
from unittest.mock import patch, Mock, MagicMock
from lib.player.bot_player import BotPlayer
from lib.game.game_interface import GameInterface
from lib.player.player_knowledge import PlayerKnowledge

class TestBotPlayer(unittest.TestCase):

    def setUp(self):
        self.game_state = Mock(
            wordlist=["HELLO", "WORLD"],
            word_length=5
        )
        self.player = BotPlayer(self.game_state)

    def test_initialization(self):
        """
        Test that the player initializes its components correctly.
        """
        self.assertIsInstance(self.player, BotPlayer)
        self.assertIsInstance(self.player.knowledge, PlayerKnowledge)
        self.assertEqual(self.player.words.list, self.game_state.wordlist)

    def test_guess_returns_valid_guess(self):
        """
        Test that the player returns a valid guess from its word list.
        """
        # Mock the word scorer to return a predictable word
        self.player.word_scorer.rank = Mock(return_value=["HELLO"])
        guess = self.player.guess(self.game_state)
        self.assertEqual(guess, "HELLO")
        self.assertIn("HELLO", self.player.guessed)

    def test_raises_exception_when_no_candidates(self):
        """
        Test that the player raises an exception when no candidates are available.
        """
        self.player.words.find_words = Mock(return_value=[])
        with self.assertRaisesRegex(Exception, "No candidates available!"):
            self.player.guess(self.game_state)

    def test_returns_when_all_letters_placed(self):
        """
        Test that the player returns the completed word if all letters are placed.
        """
        self.player.knowledge.placed = ["A", "P", "P", "L", "E"]
        guess = self.player.guess(self.game_state)
        self.assertEqual(guess, "APPLE")

    @patch('lib.player.player_knowledge.PlayerKnowledge.update_state')
    def test_update_state_delegates_to_knowledge(self, mock_update_state):
        """
        Test that the player's update_state method correctly delegates
        the call to its PlayerKnowledge instance.
        """
        mock_result = MagicMock()
        self.player.update_state(mock_result)
        mock_update_state.assert_called_once_with(mock_result)

if __name__ == '__main__':
    unittest.main()



