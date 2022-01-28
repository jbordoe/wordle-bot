import argparse

from termcolor import cprint
from alive_progress import alive_bar
from termgraph.module import Data, BarChart, Args, Colors

from lib.game_state import GameState
from lib.player.naive_player import NaivePlayer
from lib.words.simple_word_list import SimpleWordList
from lib.words.word_index import WordIndex
from lib.words.word_loader import WordLoader
from lib.stat_ranker import StatRanker

def go(runs, sample_size):
    wordlen = 5
    word_list = WordLoader.load_wordlist(sample_size=sample_size)

    print('running games')
    guesses = {}
    #words = SimpleWordList(word_list)
    words = WordIndex(word_list)
    ranker = StatRanker(word_list)
    with alive_bar(runs, bar='filling', spinner='dots') as bar:
        for i in range(runs):
            n_guesses = game(words, ranker, wordlen=wordlen)
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

def game(words, ranker, wordlen=5):
    state = GameState(words.list)
    player = NaivePlayer(state, words=words, ranker=ranker)
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
parser.add_argument(
'-s', '--sample_size', type=int, required=False, help='Number of words to sample (default: all)')

args = parser.parse_args()

runs = args.runs
sample_size = args.sample_size

go(runs, sample_size)
