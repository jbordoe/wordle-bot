import requests
from termcolor import cprint
from alive_progress import alive_bar

from lib.game_state import GameState
from lib.player.naive_player import NaivePlayer
from lib.words.simple_word_list import SimpleWordList
from lib.words.word_index import WordIndex

# TODO: find a better list without proper nouns
WORDLIST_URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words_dictionary.json"
#WORDLIST_URL = "https://raw.githubusercontent.com/matthewreagan/WebstersEnglishDictionary/master/dictionary_compact.json"

RUNS = 100

def go():
    wordlen = 5
    all_words = requests.get(WORDLIST_URL).json().keys()
    word_list = []
    for w in all_words:
        if len(w) != wordlen or set(" -").intersection(set(w)):
            continue
        w = w.upper()
        word_list.append(w)

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
    state = GameState(words.list, wordlen=wordlen)
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
