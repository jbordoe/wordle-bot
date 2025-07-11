import argparse
import logging
import multiprocessing

from termgraph.module import Args, BarChart, Colors, Data
from tqdm import tqdm

from lib.game.dummy_wordle_game import DummyWordleGame
from lib.player.nn_player import NNPlayer
from lib.word_scorer.statistical_word_scorer import StatisticalWordScorer
from lib.words.word_index import WordIndex
from lib.words.word_loader import WordLoader

# Global variables for each worker process
_word_index = None
_word_scorer = None
_word_list = WordLoader.load_wordlist()

def _initializer():
    """
    Initializes WordIndex and StatisticalWordScorer once per worker process.
    """
    global _word_index, _word_scorer
    _word_index = WordIndex(_word_list)
    _word_scorer = StatisticalWordScorer(_word_list, b=0.2)

def go(runs, sample_size, num_procs):
    print("running games")
    guesses = {}

    logging.info(f"Using {num_procs} processes for game simulation.")

    with multiprocessing.Pool(processes=num_procs, initializer=_initializer) as pool:
        with tqdm(total=runs, desc="Simulating games") as bar:
            for round_num in pool.imap_unordered(game_worker, range(runs)):
                guesses[round_num] = guesses.get(round_num, 0) + 1
                bar.update(1)
    output_results(guesses)

def game_worker(_):
    # Each worker process uses the globally initialized components
    game_state = DummyWordleGame(_word_index.list)
    # player = BotPlayer(state, words=_word_index, word_scorer=_word_scorer)
    player = NNPlayer(game_state, words=_word_index)
    result = None
    round_num = 0
    maxrounds = 10

    while True:
        round_num += 1
        guess = player.guess(game_state, prev=result)
        result = game_state.update(guess)
        player.update_state(result)

        if result.correct or round_num >= maxrounds:
            break
    return round_num

def output_results(guesses):
    print(f"""
RESULTS
    avg guesses: {float(sum(guesses.keys()) / runs)}
    max: {max(guesses)}
    min: {min(guesses)}
""")
    data_range = range(1, max(guesses.keys()) + 1)
    data_labels = [f"{i} guess" for i in data_range]
    data = [[guesses.get(i, 0)] for i in data_range]

    data = Data(data=data, labels=data_labels)

    chart = BarChart(
        data,
        Args(
            title="Guess distribution",
            colors=[Colors.Green, Colors.Red],
            space_between=False,
        ),
    )
    chart.draw()

cores = multiprocessing.cpu_count()
parser = argparse.ArgumentParser(
    description="Run several wordle games and output the results"
)
parser.add_argument(
    "-n", "--runs", type=int, required=True, help="Number of games to run"
)
parser.add_argument(
    "-s",
    "--sample_size",
    type=int,
    required=False,
    help="Number of words to sample (default: all)",
)
parser.add_argument(
    "-t",
    "--threads",
    type=int,
    default=cores,
    help=f"Number of threads to use (default: {cores})",
)

args = parser.parse_args()

threads = args.threads
runs = args.runs
sample_size = args.sample_size

if threads > multiprocessing.cpu_count():
    logging.warning(f"Requested {threads} threads, but only {cores} available.")
    threads = multiprocessing.cpu_count()

go(runs, sample_size, threads)
