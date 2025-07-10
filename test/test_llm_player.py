import unittest
import os
from unittest.mock import patch, MagicMock

from lib.player.llm_player import LLMPlayer
from lib.player.player_knowledge import PlayerKnowledge

class TestLLMPlayer(unittest.TestCase):

    def setUp(self):
        """
        Set up a mock game state and environment for each test.
        """
        self.mock_game_state = MagicMock()
        self.mock_game_state.word_length = 5

        # Patch the google.generativeai module for the duration of each test
        self.mock_genai_patcher = patch('lib.player.llm_player.genai')
        self.mock_genai = self.mock_genai_patcher.start()

        # Set a dummy API key to allow instantiation
        self.api_key_patcher = patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"})
        self.api_key_patcher.start()

        self.player = LLMPlayer(self.mock_game_state)

    def tearDown(self):
        """
        Clean up all patches after each test.
        """
        self.api_key_patcher.stop()
        self.mock_genai_patcher.stop()

    def test_instantiation(self):
        """
        Tests that LLMPlayer initializes correctly.
        """
        self.assertIsInstance(self.player.knowledge, PlayerKnowledge)
        # Check that the genai library was configured
        self.mock_genai.configure.assert_called_once_with(api_key="test-key")
        self.mock_genai.GenerativeModel.assert_called_once_with('gemini-2.0-flash')
        self.assertIsNotNone(self.player.llm)

    def test_init_with_no_api_key(self):
        """
        Tests that LLMPlayer raises an exception when the API key is not set.
        """
        # Patch the os.environ module to remove the API key
        self.api_key_patcher.stop()
        self.api_key_patcher = patch.dict(os.environ, {}, clear=True)
        self.api_key_patcher.start()

        with self.assertRaises(ValueError):
            LLMPlayer(self.mock_game_state)

    @patch('lib.player.player_knowledge.PlayerKnowledge.update_state')
    def test_update_state_delegates_to_knowledge(self, mock_update_state):
        """
        Tests that the player's update_state method correctly delegates
        the call to its PlayerKnowledge instance.
        """
        mock_result = MagicMock()
        self.player.update_state(mock_result)
        mock_update_state.assert_called_once_with(mock_result)

    def test_guess_with_valid_llm_response(self):
        """
        Tests the guess method with a valid, well-formed response from the LLM.
        """
        mock_llm_response = MagicMock()
        mock_llm_response.text = "  valid  "
        self.player.llm.generate_content.return_value = mock_llm_response

        guess = self.player.guess(self.mock_game_state)

        self.player.llm.generate_content.assert_called_once()
        self.assertEqual(guess, "VALID")
        self.assertIn("VALID", self.player.guessed)

    def test_guess_with_invalid_llm_response(self):
        """
        Tests that the guess method returns None when the LLM gives an invalid response.
        """
        self.player._generate_prompt = MagicMock(return_value="Test Prompt")

        mock_llm_response = MagicMock()
        mock_llm_response.text = "INVALID GUESS"
        self.player.llm.generate_content.return_value = mock_llm_response

        guess = self.player._generate_guess(self.mock_game_state)

        self.assertIsNone(guess)

    def test_guess_with_no_llm_response(self):
        """
        Tests that the guess method raises an exception when the LLM does not return a response.
        """
        mock_llm_response = MagicMock()
        mock_llm_response.text = ""
        self.player.llm.generate_content.return_value = mock_llm_response

        with self.assertRaises(Exception):
            self.player.guess(self.mock_game_state)

    def test_guess_with_llm_exception(self):
        """
        Tests that the guess method raises an exception when the LLM raises an exception.
        """
        mock_llm_response = MagicMock()
        mock_llm_response.text = ""
        self.player.llm.generate_content.side_effect = Exception("Test exception")

        with self.assertRaises(Exception):
            self.player.guess(self.mock_game_state)

if __name__ == '__main__':
    unittest.main()


