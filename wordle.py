import requests
from termcolor import cprint

from lib.game_state import GameState
from lib.player.naive_player import NaivePlayer

# TODO: find a better list without proper nouns
WORDLIST_URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words_dictionary.json"

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
