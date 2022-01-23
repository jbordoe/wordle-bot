import requests
import random
from termcolor import cprint

# TODO: find a better list without proper nouns
WORDLIST_URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words_dictionary.json"

class PlayerInterface:
    def guess(self, game_state, prev=None) -> str:
        pass

class HumanPlayer(PlayerInterface):
    def guess(self, game_state, prev=None) -> str:
        while True:
            print("""
Enter your guess! Must be a {}-letter word
    """.format(game_state.word_length))
            guess = input().strip().upper()
            if not guess in game_state.wordlist:
                print("Your guess is not valid")
            else:
                return guess

class NaivePlayer(PlayerInterface):
    def __init__(self, game_state):
        self.placed = ['' for _ in range(game_state.word_length)]
        self.present = set()
        self.guessed = set()
        self.excludes = [set() for _ in range(game_state.word_length)]

    def guess(self, game_state, prev=None) -> str:
        present = self.present.union(game_state.present)
        placed = [e[0] or e[1] for e in zip(self.placed, game_state.placed)]

        if prev: self._update_excludes(prev)

        placed_str = ''.join(placed)
        if len(placed_str) == game_state.word_length:
            return placed_str

        candidates = []
        # TODO: all this linear scanning is inefficient
        # Can we use/build a tree structure perhaps?
        for w in game_state.wordlist:
            invalid = False
            if w in self.guessed: continue
            for i in range(game_state.word_length):
                if placed[i] and (placed[i] != w[i]): invalid = True
                if w[i] in self.excludes[i]: invalid = True
                if invalid: break
            if invalid or not set(w).issuperset(present): continue

            candidates.append(w)

        if not candidates:
            print("WTF, no candidates available!")
        else:
            guess = random.sample(candidates, 1)[0].upper()
            self.guessed.add(guess)
            self.placed = placed
            self.present = present
            print("I guess {}".format(guess))
            return guess

    def _update_excludes(self, result):
        letters = result.letters
        for i in range(len(letters)):
            pair = letters[i]
            if not pair: continue
            l, l_state = pair
            if l_state == GameState.LETTER_STATE_PRESENT:
                self.excludes[i].add(l)

class GameGuessResult:
    def __init__(self, guess, letters=None):
        self.guess = guess
        self.letters = letters or [None for _ in range(len(guess))]

class GameState:
    LETTER_STATE_PRESENT = 0
    LETTER_STATE_PLACED = 1

    def __init__(self, wordlist, wordlen=5):
        self.wordlist = wordlist
        self.word_length = wordlen
        self.placed = ['' for _ in range(wordlen)]
        self.present = set()
        self.answer = random.sample(wordlist, 1)[0].upper()
        self.guesses = 0

    def update(self, guess):
        letters = [None for _ in range(len(guess))]
        placed_new = ['' for _ in range(self.word_length)]

        for i in range(len(guess)):
            gc = guess[i]
            if gc == self.answer[i]:
                placed_new[i] = gc
                self.present.discard(gc)
                letters[i] = (gc, self.LETTER_STATE_PLACED) 

            elif gc in self.answer:
                self.present.add(gc)
                letters[i] = (gc, self.LETTER_STATE_PRESENT) 

        self.placed = placed_new
        self.guesses += 1

        res = GameGuessResult(guess, letters=letters)
        return res

def menu():
    print("==== Menu ====")
    while True:
        print("""
    1. New game
    2. Quit
""")
        choice = input().strip()

        if choice == "1":
            game()
        elif choice == "2":
            print("Bye!")
            break
        else:
            print("Unrecognized input")


def game(wordlen=5):
    # TODO: save to a given location, only dl if not present
    all_words = requests.get(WORDLIST_URL).json().keys()
    words = [w.upper() for w in all_words if len(w) == wordlen]

    state = GameState(words, wordlen=wordlen)
#    player = HumanPlayer()
    player = NaivePlayer(state)
    print(''.join([c or "_" for c in state.placed]))

    result = None
    while True:
        print("========= GUESS #{} =========".format(state.guesses + 1))
        guess = player.guess(state, prev=result)
        result = state.update(guess)
        for pair in result.letters:
            letter, letter_state = pair if pair else (None, None)
            if letter_state == GameState.LETTER_STATE_PLACED:
                cprint(letter, 'white', 'on_green', end='')
            elif letter_state == GameState.LETTER_STATE_PRESENT:
                cprint(letter, 'white', 'on_yellow', end='')
            else:
                print('_', end='')

        if guess == state.answer:
            print("\nWELL DONE! {} guess(es)".format(state.guesses))
            return state.guesses
        print('')

# TODO: add a cool figlet banner
menu()
