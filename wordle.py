import requests
import random
from termcolor import cprint

# TODO: find a better list without proper nouns
WORDLIST_URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words_dictionary.json"

class PlayerInterface:
    def guess(self, game_state) -> str:
        pass

class HumanPlayer(PlayerInterface):
    def guess(self, game_state) -> str:
        while True:
            print("""
        Enter your guess! Must be a {}-letter word
    """.format(game_state.word_length))
            guess = input().strip().upper()
            if not guess in game_state.wordlist:
                print("Your guess is not valid")
            else:
                return guess

class GameState:
    def __init__(self, wordlist, wordlen=5):
        self.wordlist = wordlist
        self.word_length = wordlen
        self.known = ["_" for _ in range(wordlen)]
        self.found = set()
        self.answer = random.sample(wordlist, 1)[0].upper()
        self.guesses = 0

    def update(self, guess):
        known_new = [None for _ in range(self.word_length)]

        for i in range(len(guess)):
            gc = guess[i]
            if gc == self.answer[i]:
                known_new[i] = gc
                self.found.discard(gc)

            elif gc in self.answer:
                self.found.add(gc)

        self.known = known_new
        self.guesses += 1

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

    player = HumanPlayer()
    state = GameState(words, wordlen=wordlen)

    print(' '.join([c for c in state.known]))

    while True:
        print("_________ GUESS #{} _________".format(state.guesses + 1))
        guess = player.guess(state)
        for i in range(len(guess)):
            gc = guess[i]
            state.update(guess)
            if gc == state.answer[i]:
                cprint(gc, 'white', 'on_green', end='')
            elif gc in state.answer:
                cprint(gc, 'white', 'on_yellow', end='')
            else:
                print('_', end='')
        if guess == state.answer:
            print("\nWELL DONE! {} guess(es)".format(state.guesses))
            return state.guesses
        print('')

# TODO: add a cool figlet banner
menu()
