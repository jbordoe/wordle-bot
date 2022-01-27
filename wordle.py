import requests
from termcolor import cprint

from lib.game_state import GameState
from lib.player.naive_player import NaivePlayer
from lib.player.human_player import HumanPlayer
from lib.words.word_loader import WordLoader

def menu():
    print("==== Menu ====")
    while True:
        print("""
    1. New game
    2. Quit
""")
        choice = input().strip()
        words = None
        if choice == "1":
            words = WordLoader.load_wordlist() if not words else words
            game(words)
        elif choice == "2":
            print("Bye!")
            break
        else:
            print("Unrecognized input")


def game(all_words, wordlen=5):
    words = [w.upper() for w in all_words if len(w) == wordlen]

    state = GameState(words)
    player = HumanPlayer()
#    player = NaivePlayer(state, verbosity=1)
    print('' * wordlen)

    result = None
    while True:
        print("========= GUESS #{} =========".format(state.guesses + 1))
        guess = player.guess(state, prev=result)
        result = state.update(guess)
        for pair in result.letters:
            letter, letter_state = pair if pair else (None, None)
            if letter_state == GameState.LETTER_STATE_PLACED:
                cprint(letter, 'white', 'on_green', end='', attrs=['bold'])
            elif letter_state == GameState.LETTER_STATE_PRESENT:
                cprint(letter, 'white', 'on_yellow', end='', attrs=['bold'])
            else:
                print('_', end='')

        if guess == state.answer:
            print("\nWELL DONE! {} guess(es)".format(state.guesses))
            return state.guesses
        else:
            player.update_state(result)
        print('')

# TODO: add a cool figlet banner
menu()
