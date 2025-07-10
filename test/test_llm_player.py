import unittest
import os
from unittest.mock import patch, MagicMock

mock_genai = MagicMock()
with patch.dict('sys.modules', {'google.generativeai': mock_genai}):
    from lib.player.llm_player import LLMPlayer
    from lib.game.game_interface import GameInterface

class TestLLMPlayer(unittest.TestCase):

    def setUp(self):
        """
        Set up a mock game state and environment for each test.
        """
        self.mock_game_state = MagicMock()
        self.mock_game_state.word_length = 5

        self.api_key_patcher = patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"})
        self.api_key_patcher.start()
        
        self.player = LLMPlayer(self.mock_game_state)

    def tearDown(self):
        """
        Clean up patches after each test.
        """
        self.api_key_patcher.stop()
        patch.stopall()

    def test_instantiation_raises_error_if_no_api_key(self):
        """
        Tests that LLMPlayer raises a ValueError if GEMINI_API_KEY is not set.
        """
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ValueError, "GEMINI_API_KEY environment variable not set."):
                LLMPlayer(self.mock_game_state)

    def test_update_state_correctly(self):
        """
        Tests that the player's internal state is updated correctly based on a game result.
        """
        mock_result = MagicMock()
        mock_result.guess = "RAISE"
        mock_result.letters = [
            None,
            ('A', GameInterface.LETTER_STATE_PLACED),
            ('I', GameInterface.LETTER_STATE_PRESENT),
            None,
            ('E', GameInterface.LETTER_STATE_PLACED)
        ]

        self.player.update_state(mock_result)

        self.assertEqual(self.player.placed, ['', 'A', '', '', 'E'])
        self.assertEqual(self.player.present, {'I'})
        self.assertEqual(self.player.filter, {'R', 'S'})
        self.assertEqual(self.player.excludes[2], {'I'})

    @patch('google.generativeai.GenerativeModel.generate_content')
    def test_guess_with_valid_llm_response(self, mock_generate_prompt):
        """
        Tests the guess method with a valid, well-formed response from the LLM.
        """
        mock_generate_prompt.return_value = "Test Prompt"
        
        mock_llm_response = MagicMock()
        mock_llm_response.text = "  valid  "
        self.player.llm.generate_content.return_value = mock_llm_response

        guess = self.player.guess(self.mock_game_state)

        self.assertEqual(guess, "VALID")
        self.assertIn("VALID", self.player.guessed)

    @patch('lib.player.llm_player.LLMPlayer._generate_prompt')
    def test_guess_with_invalid_llm_response(self, mock_generate_prompt):
        """
        Tests that the guess method returns None when the LLM gives an invalid response.
        """
        mock_generate_prompt.return_value = "Test Prompt"
        
        mock_llm_response = MagicMock()
        mock_llm_response.text = "INVALID GUESS" # Contains a space
        self.player.llm.generate_content.return_value = mock_llm_response

        guess = self.player._generate_guess(self.mock_game_state)

        self.assertIsNone(guess)

if __name__ == '__main__':
    unittest.main()
