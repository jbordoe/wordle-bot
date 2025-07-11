import logging
import random

import torch

from lib.game.game_guess_result import GameGuessResult
from lib.nn.wordle_encoder import WordleEncoder
from lib.nn.wordle_guesser_model import WordleGuesserModel
from lib.player.player_interface import PlayerInterface
from lib.player.player_knowledge import PlayerKnowledge
from lib.words.word_index import WordIndex


class NNPlayer(PlayerInterface):
    def __init__(
        self,
        game_state,
        words: WordIndex,
        model_path: str = "models/wordle_guesser.pth"
    ):
        self.model = WordleGuesserModel()
        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()

        self.word_index = words
        self.knowledge = PlayerKnowledge(game_state.word_length)

    def guess(self, state, prev: GameGuessResult = None) -> str:
        gamestring = WordleEncoder.encode_result_letters_as_str(
            self.knowledge.letters
        )
        encoded_input = WordleEncoder.encode_game_state(gamestring)

        letter_idxs = torch.tensor([[letter_idx for (letter_idx, _) in encoded_input]])
        state_idxs = torch.tensor([[state_idx for (_, state_idx) in encoded_input]])

        with torch.no_grad():
            # For each position, get probabilities for each letter
            logits = self.model(letter_idxs, state_idxs)  # (1, 5, 26)
            # For each position, get the letter with the highest probability
            preds = logits.argmax(dim=-1)  # (1, 5)

        # Convert the letter indices to actual letters
        predicted_word_chars = [chr(c + ord('A')) for c in preds[0]]
        predicted_word = "".join(predicted_word_chars)

        # Validate the predicted word against the dictionary
        if predicted_word.lower() in self.word_index.wordset:
            return predicted_word
        else:
            logging.warning(f"Predicted word '{predicted_word}' not in dictionary.")
            logging.warning("Using fallback strategy.")
            # Fallback if NN predicts an invalid word
            # For now, just return a random valid word from the remaining possibilities
            # TODO: use a decoder to generate a valid word
            remaining_words = self.word_index.find_words(
                placed_letters=self.knowledge.placed,
                contains=list(self.knowledge.present),
                filter=self.knowledge.filter,
                excludes=self.knowledge.excludes,
            )
            if remaining_words:
                return random.choice(remaining_words).lower()
            else:
                # If no valid words left, this is an error state
                return ""

    def update_state(self, result: GameGuessResult) -> None:
        self.knowledge.update_state(result)
