import argparse
from termcolor import cprint
import time
import json

from lib.player.bot_player import BotPlayer
from lib.wordle_game import WordleGame
from lib.absurdle_game import AbsurdleGame
from lib.words.word_index import WordIndex
from lib.words.word_loader import WordLoader
from lib.stat_ranker import StatRanker

WORDLIST_PATH = "dict.json"

def init_player(state):
    words = WordLoader.load_wordlist()
    word_index = WordIndex(words)
    ranker = StatRanker(words)
    player = BotPlayer(state, words=word_index, ranker=ranker)
    return player

def go(variant='wordle', headless=False):
    state = None
    try:
        cprint("Visiting game site.", attrs=['dark'])
        game_class = WordleGame if variant == 'wordle' else AbsurdleGame
        state = game_class(headless=headless)
        player = init_player(state)

        result = None
        guesses = 0

        while True:
            cprint('Selecting a word...', attrs=['dark'])
            guess = player.guess(state, prev=result)

            if not guess:
                print(result.letters)
                raise Exception("Could not find a word!", 'red')

            cprint(f'Guess #{guesses+1} is {guess}', 'cyan', attrs=['bold'])

            cprint("Checking results...", attrs=['dark'])
            result = state.update(guess)

            if not result:
                cprint("Guess was invalid, trying something else", 'yellow')
            else:
                guesses += 1
                if result.correct:
                    cprint("Solution found!", 'green')
                    print(result.text)
                    print("Closing browser in 30 seconds")
                    time.sleep(30)
                    break
                else:
                    cprint("Updating...", attrs=['dark'])
                    player.update_state(result)

            if state.max_guesses and guesses >= state.max_guesses:
                cprint("Could not find the solution!", 'red')
                print(result.text)
                break
    finally:
        if state: state.quit()


parser=argparse.ArgumentParser(description='Have a bot play wordle (or a variant) in the browser')
parser.add_argument(
    '--headless', action='store_true', help='Run with a visible browser')
parser.add_argument(
    '-v', '--variant', type=str, required=False, default='wordle', help='Number of games to run')

args = parser.parse_args()

variant = 'wordle'
if args.variant not in ('wordle', 'absurdle'):
    raise Exception(f"Invalid variant {variant}")
else:
    variant = args.variant

go(
    variant=variant,
    headless=args.headless,
)
