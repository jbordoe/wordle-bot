import requests
from termcolor import cprint
from alive_progress import alive_bar

from lib.game_state import GameState
from lib.player.naive_player import NaivePlayer
from lib.words.simple_word_list import SimpleWordList
from lib.words.word_index import WordIndex
from lib.words.word_loader import WordLoader

RUNS = 1000

def go():
    wordlen = 5
    word_list = WordLoader.load_wordlist()

    print('running games')
    guesses = []
    #words = SimpleWordList(word_list)
    words = WordIndex(word_list)
    with alive_bar(RUNS, bar='filling', spinner='dots') as bar:
        for i in range(RUNS):
            n_guesses = game(words, wordlen)
            guesses.append(n_guesses)
            bar()

    print(f"""
RESULTS
    avg guesses: {float(sum(guesses) / RUNS)}
    max: {max(guesses)}
    min: {min(guesses)}
""")
    # TODO: plot distribution of guesses

def game(words, wordlen=5):
    state = GameState(words.list)
    player = NaivePlayer(state, words=words)
    result = None
    while True:
        guess = player.guess(state, prev=result)
        result = state.update(guess)

        if guess == state.answer:
            return state.guesses
        else:
            player.update_state(result)

go()
