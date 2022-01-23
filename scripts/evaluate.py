import requests
from termcolor import cprint
from alive_progress import alive_bar

from lib.game_state import GameState
from lib.player.naive_player import NaivePlayer

# TODO: find a better list without proper nouns
WORDLIST_URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words_dictionary.json"

RUNS = 100

def go():
    wordlen = 5
    all_words = requests.get(WORDLIST_URL).json().keys()
    words = [w.upper() for w in all_words if len(w) == wordlen]

    print('running games')
    guesses = []
    with alive_bar(RUNS, bar='filling', spinner='dots') as bar:
        for i in range(RUNS):
            n_guesses = game(words, wordlen)
            guesses.append(n_guesses)
            bar()

    print("""
    RESULTS
        avg guesses: {}
        max: {}
        min: {}
""".format(float(sum(guesses)) / RUNS, max(guesses), min(guesses)))
    # TODO: plot distribution of guesses

def game(words, wordlen=5):
    state = GameState(words, wordlen=wordlen)
    player = NaivePlayer(state)
    result = None
    while True:
        guess = player.guess(state, prev=result)
        result = state.update(guess)

        if guess == state.answer:
            return state.guesses
        else:
            player.update_state(result)

go()
