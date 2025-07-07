import unittest
from unittest.mock import patch, Mock
import requests

from lib.words.word_loader import WordLoader

class TestWordLoader(unittest.TestCase):

    @patch('lib.words.word_loader.requests.get')
    def test_load_wordlist_successfully(self, mock_get):
        mock_response1 = Mock()
        mock_response1.text = "apple\nbanana"
        
        mock_response2 = Mock()
        mock_response2.text = "banana\ncherry"

        # Set the side_effect to return the mock responses in order
        mock_get.side_effect = [mock_response1, mock_response2]

        words = WordLoader.load_wordlist()

        self.assertEqual(set(words), {"APPLE", "BANANA", "CHERRY"})
        self.assertEqual(mock_get.call_count, 2)

    @patch('lib.words.word_loader.requests.get')
    def test_load_wordlist_with_sample_size(self, mock_get):
        mock_response1 = Mock()
        mock_response1.text = "one\ntwo\nthree\nfour\nfive"
        mock_response2 = Mock()
        mock_response2.text = "" # No new words
        mock_get.side_effect = [mock_response1, mock_response2]

        words = WordLoader.load_wordlist(sample_size=3)

        self.assertEqual(len(words), 3)
        self.assertTrue(set(words).issubset({"ONE", "TWO", "THREE", "FOUR", "FIVE"}))

    @patch('lib.words.word_loader.requests.get')
    def test_network_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        with self.assertRaises(requests.exceptions.RequestException):
            WordLoader.load_wordlist()

if __name__ == '__main__':
    unittest.main()
