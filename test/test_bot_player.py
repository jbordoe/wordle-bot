import unittest
from unittest.mock import patch, Mock
from lib.player.bot_player import BotPlayer
from lib.game.game_interface import GameInterface

class TestBotPlayer(unittest.TestCase):

    def setUp(self):
        self.game_state = Mock(
            wordlist=["HELLO", "WORLD"],
            word_length=5
        )
        self.player = BotPlayer(self.game_state)

    def test_initialization(self):
        """
        Test that the player can be initialized with a game state
        """
        self.assertIsInstance(self.player, BotPlayer)
        self.assertEqual(self.player.words.list, self.game_state.wordlist)

    def test_initialization_with_words(self):
        """
        Test that the player can be initialized with a game state and a word list
        """
        words = ["HELLO", "WORLD", "FOO"]
        words_obj = Mock(list=words)
        player = BotPlayer(self.game_state, words=words_obj)
        self.assertIsInstance(player, BotPlayer)
        self.assertEqual(player.words.list, words)

    def test_guess_returns_valid_guess(self):
        """
        Test that the player returns a valid guess
        """
        guess = self.player.guess(self.game_state)
        self.assertTrue(guess in self.game_state.wordlist)
        self.assertTrue(guess in self.player.guessed)

    def test_raises_exception_when_no_candidates(self):
        """
        Test that the player raises an exception when no candidates are available
        """
        words_obj = Mock(list=[], find_words=Mock(return_value=[]))
        player = BotPlayer(self.game_state, words=words_obj)
        with self.assertRaises(Exception):
            player.guess(self.game_state)

    def test_returns_when_all_letters_placed(self):
        """
        Test that the player returns when all letters are placed
        """
        player = BotPlayer(self.game_state)
        result = Mock(
            guess="APPLE",
            letters=[(l, GameInterface.LETTER_STATE_PLACED) for l in "APPLE"]
        )
        player.update_state(result)
        guess = player.guess(self.game_state)
        self.assertEqual(guess, "APPLE")

    def test_update_state(self):
        """
        Test that the player updates the state
        """
        result = Mock(
            guess="HAPPY",
            letters=[
                ("H", GameInterface.LETTER_STATE_PLACED),
                ("A", GameInterface.LETTER_STATE_PRESENT),
                ("P", GameInterface.LETTER_STATE_ABSENT),
                ("P", GameInterface.LETTER_STATE_ABSENT),
                ("Y", GameInterface.LETTER_STATE_ABSENT)
            ]
        )
        self.player.update_state(result)
        self.assertEqual(self.player.placed, ["H", '', '', '', ''])
        self.assertEqual(self.player.present, set(["A"]))
        self.assertEqual(self.player.filter, set(["P", "Y"]))
        self.assertEqual(self.player.excludes, [set(), set(["A"]), set(), set(), set()])
if __name__ == '__main__':
    unittest.main()


