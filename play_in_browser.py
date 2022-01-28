import time
import json

from lib.player.naive_player import NaivePlayer
from lib.browser_game import BrowserGame
from lib.words.word_index import WordIndex
from lib.words.word_loader import WordLoader
from lib.stat_ranker import StatRanker

WORDLIST_PATH = "dict.json"

def init_player(state):
    words = WordLoader.load_wordlist()
    word_index = WordIndex(words)
    ranker = StatRanker(words)
    player = NaivePlayer(state, words=word_index, ranker=ranker)
    return player

def go():
    state = None
    try:
        print("Visiting wordle site")
        state = BrowserGame(headless=False) 
        player = init_player(state)

        result = None
        guesses = 0 

        while True:
            print('Selecting a word...')
            guess = player.guess(state, prev=result)

            if not guess:
                print(result.letters)
                raise Exception("Could not find a word!")

            print(f'Guess #{guesses+1} is {guess}')

            print("Checking results...")
            result = state.update(guess)

            if not result:
                print("Guess was invalid, trying something else")
            else:
                guesses += 1
                if result.correct:
                    print("Wordle found!")
                    print(result.text)
                    print("Closing browser in 30 seconds")
                    time.sleep(30)
                    break
                else:
                    print("Updating...")
                    player.update_state(result)

            if guesses == 6:
                print("Could not find the Wordle!")
                break
    finally:
        if state: state.quit()

go()
