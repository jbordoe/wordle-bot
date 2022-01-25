import random

from lib.player.player_interface import PlayerInterface
from lib.game_state import GameState
from lib.words.simple_word_list import SimpleWordList

class NaivePlayer(PlayerInterface):
    def __init__(self, game_state):
        self.placed = ['' for _ in range(game_state.word_length)]
        self.present = set()
        self.guessed = set()
        self.filter = set()
        self.excludes = [set() for _ in range(game_state.word_length)]
        self.words = SimpleWordList(game_state.wordlist)

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
            guess = random.sample(candidates, 1)[0].upper()
            self.guessed.add(guess)
            #self.candidates.remove(guess)
            return guess

    def update_state(self, result) -> None:
        letters = result.letters
        guess = result.guess
        for i in range(len(letters)):
            pair = letters[i]
            if not pair:
                self.filter.add(guess[i])
                continue
            l, l_state = pair
            if l_state == GameState.LETTER_STATE_PRESENT:
                self.excludes[i].add(l)
                self.present.add(l)
            elif l_state == GameState.LETTER_STATE_PLACED:
                self.placed[i] = l
                # TODO: how do wa account for the possibility
                # that a placed letter occurs again?
                self.present.discard(l)
