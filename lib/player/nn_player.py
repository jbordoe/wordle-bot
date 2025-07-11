
import torch
import torch.nn.functional as F

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
        self.wordset = set(words.list)
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
            guesses = self._decode_with_filter(logits)
            return guesses[0]
            # For each position, get the letter with the highest probability
            # preds = logits.argmax(dim=-1)  # (1, 5)

    def update_state(self, result: GameGuessResult) -> None:
        self.knowledge.update_state(result)

    def _decode_with_filter(self, logits):
        """
        logits: (batch_size, 5, 26) — raw output from the model

        Returns: best guess from wordlist for each input in batch
        """
        B = logits.size(0)
        guesses = []

        new_words = list(self.wordset - set(self.knowledge.previous_guesses()))
        word_tensor = torch.tensor(
            [
                [ord(char) - ord('A') for char in word]
                for word in new_words
            ]
        )
        for b in range(B):
            # Score each word in wordlist using sum of log-probs
            probs = F.log_softmax(logits[b], dim=-1)  # (5, 26)
            scores = torch.gather(probs, 1, word_tensor.T).sum(dim=0)  # (W,)
            best_idx = torch.argmax(scores).item()
            guesses.append(new_words[best_idx])

        return guesses
