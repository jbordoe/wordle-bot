import argparse
import logging
import multiprocessing
import random
import sys

from tqdm import tqdm

from lib.game.dummy_wordle_game import DummyWordleGame
from lib.nn.wordle_encoder import WordleEncoder
from lib.player.bot_player import BotPlayer
from lib.word_scorer.statistical_word_scorer import StatisticalWordScorer
from lib.words.word_index import WordIndex
from lib.words.word_loader import WordLoader

# Redirect tqdm output stream to stderr
tqdm.write = lambda x: sys.stderr.write(x + '\n')

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


def game_worker(_):
    # Each worker process uses the globally initialized components
    wordlen = 5

    state = DummyWordleGame(_word_index.list)
    player = BotPlayer(state, words=_word_index, word_scorer=_word_scorer)
    result = None
    stateobjs = []
    round_num = 0
    maxrounds = 6

    while True:
        gamestring = WordleEncoder.encode_result_letters_as_str(
            player.knowledge.letters
        )
        stateobj = {
            "input": {
                "previous_guesses": [s["output"] for s in stateobjs],
                "correct_answer": state.answer,
                "word_length": wordlen,
                "gamestring": gamestring,
            },
        }
        round_num += 1
        if round_num >= maxrounds:
            guess = state.answer
        else:
            guess = player.guess(state, prev=result)

        result = state.update(guess)
        player.update_state(result)

        stateobj['output'] = guess
        stateobjs.append(stateobj)

        if result.correct or round_num >= maxrounds:
            break
    return stateobjs


def go(runs, sample_size):
    logging.info("running games")

    game_states = []
    num_procs = multiprocessing.cpu_count()
    logging.info(f"Using {num_procs} processes for game simulation.")

    with multiprocessing.Pool(processes=num_procs, initializer=_initializer) as pool:
        with tqdm(total=runs, desc="Simulating games") as bar:
            for states in pool.imap_unordered(game_worker, range(runs)):
                game_states.extend(states)
                bar.update(1)

    # take a random sample of game states
    states_sample = random.sample(game_states, sample_size)

    logging.info("generating output")
    output_results(states_sample)


def output_results(game_states):
    for state in game_states:
        statestr = f"{state['input']['gamestring']} -> {state['output']}"
        print(statestr)

parser = argparse.ArgumentParser(
    description="Generate wordle game training data"
)
parser.add_argument(
    "-n", "--runs", type=int, required=True, help="Number of games to run"
)
parser.add_argument(
    "-s", "--sample", type=int, default=100, help="Number of moves to sample"
)

args = parser.parse_args()

runs = args.runs
sample_size = args.sample

go(runs, sample_size)


