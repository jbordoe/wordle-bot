import argparse
import sys
from termcolor import cprint
from pyfiglet import Figlet

from lib.game.dummy_wordle_game import DummyWordleGame
from lib.game.game_interface import GameInterface 
from lib.player.bot_player import BotPlayer
from lib.player.human_player import HumanPlayer
from lib.word_scorer.statistical_word_scorer import StatisticalWordScorer
from lib.words.word_loader import WordLoader

def menu(player_type='human', verbosity=1):
    cprint("Menu:", attrs=['bold', 'underline'])
    while True:
        print("""
    1. New game
    2. Quit
""")
        choice = input().strip()
        words = None
        if choice == "1":
            sys.stdout.write("\033[F")
            words = WordLoader.load_wordlist() if not words else words
            game(words, player_type, verbosity=verbosity)
        elif choice == "2":
            sys.stdout.write("\033[F")
            print("Bye!")
            break
        else:
            sys.stdout.write("\033[F")
            print("Unrecognized input")


def game(words, player_type, wordlen=5, verbosity=1):
    state = DummyWordleGame(words)
    player = None
    if player_type == 'human':
        player = HumanPlayer()
    else:
        word_scorer = StatisticalWordScorer(words, b=0.7)
        player = BotPlayer(
            state,
            word_scorer=word_scorer,
            verbosity=verbosity
        )
    print('_' * wordlen)

    result = None
    while True:
        guess = player.guess(state, prev=result)
        result = state.update(guess)
        for i, pair in enumerate(result.letters):
            letter, letter_state = pair if pair else (None, None)
            if letter_state == GameInterface.LETTER_STATE_PLACED:
                cprint(letter, 'white', 'on_green', end='', attrs=['bold'])
            elif letter_state == GameInterface.LETTER_STATE_PRESENT:
                cprint(letter, 'white', 'on_yellow', end='', attrs=['bold'])
            else:
                cprint(guess[i], end='')

        if guess == state.answer:
            cprint(f"\nSolved! {state.guesses} guess(es)", 'green')
            return state.guesses
        else:
            player.update_state(result)
        print('')

f = Figlet(font='roman')
cprint("\n" + f.renderText('Wordle'), 'cyan')

parser=argparse.ArgumentParser(description='Play wordle on the command line.')
parser.add_argument(
    '-p', '--player', type=str, required=False, default='human', help='Type of player (human or bot)')

parser.add_argument(
    '-v', '--verbosity', type=int, required=False, default=1, help='How much text to output')
args = parser.parse_args()

player = 'human'
if args.player not in ('human', 'bot'):
    raise Exception(f"Invalid player {player}")

menu(
    player_type=args.player,
    verbosity=args.verbosity
)
