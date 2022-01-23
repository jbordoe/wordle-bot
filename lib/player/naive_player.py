import random

from lib.player.player_interface import PlayerInterface
from lib.game_state import GameState

class NaivePlayer(PlayerInterface):
    def __init__(self, game_state):
        self.placed = ['' for _ in range(game_state.word_length)]
        self.present = set()
        self.guessed = set()
        self.excludes = [set() for _ in range(game_state.word_length)]

    def guess(self, game_state, prev=None) -> str:
        placed_str = ''.join(self.placed)
        if len(placed_str) == game_state.word_length:
            return placed_str

        candidates = []
        # TODO: all this linear scanning is inefficient
        # Can we use/build a tree structure perhaps?
        for w in game_state.wordlist:
            invalid = False
            if w in self.guessed: continue
            for i in range(game_state.word_length):
                if self.placed[i] and self.placed[i] != w[i]: invalid = True
                if w[i] in self.excludes[i]: invalid = True
                if invalid: break
            if invalid or not set(w).issuperset(self.present): continue

            candidates.append(w)

        if not candidates:
            # TODO: throw a proper exception here
            print("WTF, no candidates available!")
        else:
            guess = random.sample(candidates, 1)[0].upper()
            self.guessed.add(guess)
            return guess

    def update_state(self, result) -> None:
        letters = result.letters
        for i in range(len(letters)):
            pair = letters[i]
            if not pair: continue
            l, l_state = pair
            if l_state == GameState.LETTER_STATE_PRESENT:
                self.excludes[i].add(l)
                self.present.add(l)
            elif l_state == GameState.LETTER_STATE_PLACED:
                self.placed[i] = l
                # TODO: how do wa account for the possibility
                # that a placed letter occurs again?
                self.present.discard(l)
