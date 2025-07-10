import logging

from lib.player.player_interface import PlayerInterface
from lib.player.player_knowledge import PlayerKnowledge
from lib.word_scorer.random_word_scorer import RandomWordScorer
from lib.words.simple_word_list import SimpleWordList


class BotPlayer(PlayerInterface):
    def __init__(self, game_state, words=None, word_scorer=None):
        self.knowledge = PlayerKnowledge(game_state.word_length)
        self.guessed = set()
        self.words = words or SimpleWordList(game_state.wordlist)
        self.word_scorer = word_scorer or RandomWordScorer(game_state.wordlist)

    def guess(self, game_state, prev=None) -> str:
        placed_str = "".join(
            letter if letter else "" for letter in self.knowledge.placed
        )
        if len(placed_str) == game_state.word_length:
            return placed_str

        candidates = self.words.find_words(
            placed_letters=self.knowledge.placed,
            contains=self.knowledge.present,
            filter=self.knowledge.filter,
            excludes=self.knowledge.excludes,
        )

        if not candidates:
            raise Exception("No candidates available!")
        else:
            candidates = list(set(candidates).difference(self.guessed))
            guess = self.word_scorer.rank(candidates)[0]
            logging.debug(f"guess = {guess}")

            self.guessed.add(guess)
            return guess

    def update_state(self, result) -> None:
        self.knowledge.update_state(result)
