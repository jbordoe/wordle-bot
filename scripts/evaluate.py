import argparse

from termcolor import cprint
from alive_progress import alive_bar
from termgraph.module import Data, BarChart, Args, Colors

from lib.game_state import GameState
from lib.player.naive_player import NaivePlayer
from lib.words.simple_word_list import SimpleWordList
from lib.words.word_index import WordIndex
from lib.words.word_loader import WordLoader

def go(runs):
    wordlen = 5
    word_list = WordLoader.load_wordlist()

    print('running games')
    guesses = {}
    #words = SimpleWordList(word_list)
    words = WordIndex(word_list)
    with alive_bar(runs, bar='filling', spinner='dots') as bar:
        for i in range(runs):
            n_guesses = game(words, wordlen)
            if n_guesses in guesses:
                guesses[n_guesses] += 1
            else:
                guesses[n_guesses] = 1
            bar()
    output_results(guesses)

def output_results(guesses):
    print(f"""
RESULTS
    avg guesses: {float(sum(guesses.keys()) / runs)}
    max: {max(guesses)}
    min: {min(guesses)}
""")
    data_range = range(1, max(guesses.keys())+1)
    data_labels = [f'{i} guess' for i in data_range]
    data = [[guesses.get(i, 0)] for i in data_range]

    data = Data(
        data=data,
        labels=data_labels
    )

    chart = BarChart(
        data,
        Args(
            title="Guess distribution",
            colors=[Colors.Green, Colors.Red],
            space_between=False
        )
    )
    chart.draw()

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

parser=argparse.ArgumentParser(description='Run several wordle games and output the results')
parser.add_argument(
    '-n', '--runs', type=int, required=True, help='Number of games to run')

args = parser.parse_args()

runs = args.runs

go(runs)
