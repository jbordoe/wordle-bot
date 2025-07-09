import argparse
from termcolor import cprint, colored
import logging
import random
import re
import time

from lib.player.bot_player import BotPlayer
from lib.player.llm_player import LLMPlayer
from lib.game.wordle_game import WordleGame
from lib.game.absurdle_game import AbsurdleGame
from lib.word_scorer.statistical_word_scorer import StatisticalWordScorer
from lib.words.word_loader import WordLoader
from lib.words.word_index import WordIndex

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

def init_player(state, play_with_llm=False):
    words = WordLoader.load_wordlist()
    word_index = WordIndex(words)
    word_scorer = StatisticalWordScorer(words, b=0.5)

    if play_with_llm:
        logging.info("initializing LLM player...")
        return LLMPlayer(state, words=word_index, word_scorer=word_scorer)
    else:
        logging.info("initializing Bot player...")
        return BotPlayer(state, words=word_index, word_scorer=word_scorer)
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


def go(
    variant='wordle',
    headless=False,
    theme='default',
    initial_guesses=[],
    play_with_llm=False
):
    state = None
    try:
        logging.info("Visiting game site.")
        game_class = WordleGame if variant == 'wordle' else AbsurdleGame
        state = game_class(headless=headless)
        player = init_player(state, play_with_llm=play_with_llm)

        result = None
        n_guesses = 0

        while True:
            logging.info('Selecting a word...')
            if initial_guesses:
                guess = initial_guesses.pop(0)
            else:
                guess = player.guess(state, prev=result)

            if not guess:
                print(result.letters)
                raise Exception("Could not find a word!")

            guess_for_print = colored(guess, 'yellow', attrs=['bold', 'underline'])
            logging.info(f'Guess #{n_guesses+1} is {guess_for_print}')

            logging.info("Checking results...")
            result = state.update(guess)

            if not result:
                logging.warning("Guess was invalid, trying something else")
            else:
                n_guesses += 1
                if result.correct:
                    logging.info("Solution found!")
                    print(map_result(result.text, theme))
                    if not headless:
                        logging.info("Closing browser in 30 seconds")
                        time.sleep(30)
                    break
                else:
                    logging.info("Updating...")
                    player.update_state(result)

            if state.max_guesses and n_guesses >= state.max_guesses:
                logging.error("Could not find the solution!")
                print(result.text)
                break
    finally:
        if state: state.quit()


parser=argparse.ArgumentParser(description='Have a bot play wordle (or a variant) in the browser')
parser.add_argument(
    '--headless', action='store_true', help='Run with a visible browser')
parser.add_argument('--llm', action='store_true', help='Use the Gemini LLM to generate guesses')
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
    theme=args.theme,
    play_with_llm=args.llm
)
