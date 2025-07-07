import random

from lib.player.player_interface import PlayerInterface
from lib.game_state_interface import GameStateInterface 
from lib.words.simple_word_list import SimpleWordList
from lib.words.word_index import WordIndex
from lib.word_scorer.random_word_scorer import RandomWordScorer

class BotPlayer(PlayerInterface):
    def __init__(self, game_state, words=None, word_scorer=None, verbosity=0):
        self.placed = ['' for _ in range(game_state.word_length)]
        self.present = set()
        self.guessed = set()
        self.filter = set()
        self.excludes = [set() for _ in range(game_state.word_length)]
        self.words = words or SimpleWordList(game_state.wordlist)
        self.word_scorer = word_scorer or RandomWordScorer(game_state.wordlist)
        self.verbosity = verbosity

    def guess(self, game_state, prev=None) -> str:
        placed_str = ''.join(self.placed)
        if len(placed_str) == game_state.word_length:
            return placed_str

        candidates = self.words.find_words(
            placed_letters=self.placed,
            contains=self.present,
            filter=self.filter,
            excludes=self.excludes
        )

        if not candidates:
            # TODO: throw a proper exception here
            print("WTF, no candidates available!")
        else:
            candidates = list(set(candidates).difference(self.guessed))
            guess = self.word_scorer.rank(candidates)[0]
            self.guessed.add(guess)
            if self.verbosity:
                print(f"guess = {guess}")
            return guess

    def update_state(self, result) -> None:
        letters = result.letters
        guess = result.guess
        seen = set()
        for i, pair in enumerate(letters):
            if not pair:
                if not guess[i] in seen: self.filter.add(guess[i])
                continue
            l, l_state = pair
            if l_state == GameStateInterface.LETTER_STATE_PRESENT:
                self.excludes[i].add(l)
                self.present.add(l)
                self.filter.discard(l)
            elif l_state == GameStateInterface.LETTER_STATE_PLACED:
                self.placed[i] = l
                # TODO: how do wa account for the possibility
                # that a placed letter occurs again?
                self.filter.discard(l)
                self.present.discard(l)
            seen.add(guess[i])
