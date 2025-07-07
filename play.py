import argparse
from termcolor import cprint
import time
import json
import random
import re

from lib.player.bot_player import BotPlayer
from lib.wordle_game import WordleGame
from lib.game.absurdle_game import AbsurdleGame
from lib.word_scorer.statistical_word_scorer import StatisticalWordScorer
from lib.words.word_loader import WordLoader
from lib.words.word_index import WordIndex

WORDLIST_PATH = "dict.json"

THEMES = {
    'default': {'absent': '⬛', 'present': '🟨', 'placed': '🟩', 'dark': True},
    'animals': {'absent': '🐁', 'present': '🐤', 'placed': '🐸', 'dark': False},
    'hearts':  {'absent': '🖤', 'present': '💛', 'placed': '💚', 'dark': True},
    'circles': {'absent': '⚫️', 'present': '🟡', 'placed': '🟢', 'dark': True},
    'clothes': {'absent': '🎩', 'present': '🩳', 'placed': '🩲', 'dark': True},
    'food':    {'absent': '🥚', 'present': '🍋', 'placed': '🍏', 'dark': False},
    'emoji':   {'absent': '☹️',  'present': '😐', 'placed': '🙂', 'dark': False},
    'smile':   {'absent': '😐', 'present': '🙂', 'placed': '😃', 'dark': False},
    'tree':    {'absent': '🌱', 'present': '🌿', 'placed': '🌳', 'dark': False},
    'bird':    {'absent': '🥚', 'present': '🐣', 'placed': '🐓', 'dark': False},
    'medals':  {'absent': '🥉', 'present': '🥈', 'placed': '🥇', 'dark': False},
    'moon1':   {'absent': '🌑', 'present': '🌗', 'placed': '🌕', 'dark': False},
    'moon2':   {'absent': '🌚', 'present': '🌜', 'placed': '🌝', 'dark': False},
    'weather': {'absent': '⛈', 'present': '🌥', 'placed': '🌞', 'dark': False},
    'foodmix': {'absent': '🥚🦴🍚🥛🎂', 'present': '🧀🍌🍋🥐', 'placed': '🥬🥦🥒🥝🍏', 'dark': False},
    'misc': {
        'absent':  '🌚💣🏴🎮🎱🔌📞',
        'present': '🍯🎷🛵🚜🔑🧽🛎📒🙃🦶',
        'placed':  '🤢🍀🥝🪀🔋🦠📗✅🔫',
        'dark': True
    },
}
VALID_THEMES = list(THEMES.keys()) + ['random', 'shuffle']

def init_player(state):
    words = WordLoader.load_wordlist()
    word_index = WordIndex(words)
    word_scorer = StatisticalWordScorer(words, b=0.5)
    player = BotPlayer(state, words=word_index, word_scorer=word_scorer)
    return player

def map_result(result, theme):
    if theme == 'random': theme = random.choice(list(THEMES.keys()))
    if theme in [None, 'default']: return result

    if theme == 'shuffle':
        dark = random.choice([True, False])
        tmap = {}
        for key in ['absent', 'present', 'placed']:
             tmap[THEMES['default'][key]] = ''.join([THEMES[t][key] for t in THEMES if THEMES[t]['dark'] == dark])

        tmap['⬜'] = tmap.get('⬛')
        result = [random.choice(tmap[c]) if c in tmap else c for c in result]
        result = ''.join(result)
    else:
        for key in ['absent', 'present', 'placed']:
            new = random.choice(THEMES[theme][key])
            if key == 'absent': result = result.replace('⬜', new)
            result = result.replace(THEMES['default'][key], new)
    return result


def go(variant='wordle', headless=False, theme='default', initial_guesses=[]):
    state = None
    try:
        cprint("Visiting game site.", attrs=['dark'])
        game_class = WordleGame if variant == 'wordle' else AbsurdleGame
        state = game_class(headless=headless)
        player = init_player(state)

        result = None
        n_guesses = 0

        while True:
            cprint('Selecting a word...', attrs=['dark'])
            if initial_guesses:
                guess = initial_guesses.pop(0)
            else:
                guess = player.guess(state, prev=result)

            if not guess:
                print(result.letters)
                raise Exception("Could not find a word!", 'red')

            cprint(f'Guess #{n_guesses+1} is {guess}', 'cyan', attrs=['bold'])

            cprint("Checking results...", attrs=['dark'])
            result = state.update(guess)

            if not result:
                cprint("Guess was invalid, trying something else", 'yellow')
            else:
                n_guesses += 1
                if result.correct:
                    cprint("Solution found!", 'green')
                    print(map_result(result.text, theme))
                    if not headless:
                        print("Closing browser in 30 seconds")
                        time.sleep(30)
                    break
                else:
                    cprint("Updating...", attrs=['dark'])
                    player.update_state(result)

            if state.max_guesses and n_guesses >= state.max_guesses:
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
parser.add_argument(
    '-g', '--guesses', type=str, required=False, default=None, help='Comma-separated list of initial guesses.')
parser.add_argument(
    '-t', '--theme',
    type=str,
    required=False,
    default='default',
    help=f"Theme for progress output. (Options: {','.join(VALID_THEMES)})"
)

args = parser.parse_args()

initial_guesses = []
variant = 'wordle'
if args.variant not in ('wordle', 'absurdle'):
    raise Exception(f"Invalid variant: {variant}")
else:
    variant = args.variant

if args.theme not in VALID_THEMES:
    raise Exception(f"Invalid theme: {args.theme}")

if args.guesses:
    if re.match(r'[a-zA-Z]{5}(,[a-zA-Z]{5})*', args.guesses):
        initial_guesses = args.guesses.upper().split(',')
    else:
        raise Exception("Invalid guesses!")

go(
    variant=variant,
    headless=args.headless,
    initial_guesses=initial_guesses,
    theme=args.theme
)
