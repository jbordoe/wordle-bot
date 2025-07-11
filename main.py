import argparse
import logging
import random
import re
import time

from pyfiglet import Figlet
from termcolor import colored, cprint

from lib.game.absurdle_game import AbsurdleGame
from lib.game.dummy_wordle_game import DummyWordleGame
from lib.game.wordle_game import WordleGame
from lib.player.bot_player import BotPlayer
from lib.player.human_player import HumanPlayer
from lib.player.llm_player import LLMPlayer
from lib.word_scorer.statistical_word_scorer import StatisticalWordScorer
from lib.words.word_index import WordIndex
from lib.words.word_loader import WordLoader

THEMES = {
    "default": {"absent": "⬛", "present": "🟨", "placed": "🟩", "dark": True},
    "animals": {"absent": "🐁", "present": "🐤", "placed": "🐸", "dark": False},
    "hearts": {"absent": "🖤", "present": "💛", "placed": "💚", "dark": True},
    "circles": {"absent": "⚫️", "present": "🟡", "placed": "🟢", "dark": True},
    "clothes": {"absent": "🎩", "present": "🩳", "placed": "🩲", "dark": True},
    "food": {"absent": "🥚", "present": "🍋", "placed": "🍏", "dark": False},
    "emoji": {"absent": "☹️", "present": "😐", "placed": "🙂", "dark": False},
    "smile": {"absent": "😐", "present": "🙂", "placed": "😃", "dark": False},
    "tree": {"absent": "🌱", "present": "🌿", "placed": "🌳", "dark": False},
    "bird": {"absent": "🥚", "present": "🐣", "placed": "🐓", "dark": False},
    "medals": {"absent": "🥉", "present": "🥈", "placed": "🥇", "dark": False},
    "moon1": {"absent": "🌑", "present": "🌗", "placed": "🌕", "dark": False},
    "moon2": {"absent": "🌚", "present": "🌜", "placed": "🌝", "dark": False},
    "weather": {"absent": "⛈", "present": "🌥", "placed": "🌞", "dark": False},
    "foodmix": {
        "absent": "🥚🦴🍚🥛🎂",
        "present": "🧀🍌🍋🥐",
        "placed": "🥬🥦🥒🥝🍏",
        "dark": False,
    },
    "misc": {
        "absent": "🌚💣🏴🎮🎱🔌📞",
        "present": "🍯🎷🛵🚜🔑🧽🛎📒🙃🦶",
        "placed": "🤢🍀🥝🪀🔋🦠📗✅🔫",
        "dark": True,
    },
}
VALID_THEMES = list(THEMES.keys()) + ["random", "shuffle"]


def init_player(state, player_type):
    words = WordLoader.load_wordlist()
    word_index = WordIndex(words)
    word_scorer = StatisticalWordScorer(words, b=0.5)

    if player_type == "human":
        return HumanPlayer()
    elif player_type == "bot":
        logging.info("initializing Bot player...")
        return BotPlayer(state, words=word_index, word_scorer=word_scorer)
    elif player_type == "llm":
        logging.info("initializing LLM player...")
        return LLMPlayer(state, words=word_index)
    else:
        raise Exception(f"Invalid player type: {player_type}")


def map_result(result, theme):
    if theme == "random":
        theme = random.choice(list(THEMES.keys()))
    if theme in [None, "default"]:
        return result

    if theme == "shuffle":
        dark = random.choice([True, False])
        tmap = {}
        for key in ["absent", "present", "placed"]:
            tmap[THEMES["default"][key]] = "".join(
                [THEMES[t][key] for t in THEMES if THEMES[t]["dark"] == dark]
            )

        tmap["⬜"] = tmap.get("⬛")
        result = [random.choice(tmap[c]) if c in tmap else c for c in result]
        result = "".join(result)
    else:
        for key in ["absent", "present", "placed"]:
            new = random.choice(THEMES[theme][key])
            if key == "absent":
                result = result.replace("⬜", new)
            result = result.replace(THEMES["default"][key], new)
    return result


def console_game(player_type, wordlen=5, initial_guesses=[], theme="default"):
    words = WordLoader.load_wordlist()
    state = DummyWordleGame(words)
    player = init_player(state, player_type)

    print("-" * wordlen)

    result = None
    while True:
        if initial_guesses:
            guess = initial_guesses.pop(0)
        else:
            guess = player.guess(state, prev=result)
        result = state.update(guess)
        for i, letter_obj in enumerate(result.letters):
            if letter_obj.is_placed():
                cprint(letter_obj.value, "white", "on_green", end="", attrs=["bold"])
            elif letter_obj.is_present():
                cprint(letter_obj.value, "white", "on_yellow", end="", attrs=["bold"])
            else:
                cprint(letter_obj.value, end="")

        if guess == state.answer:
            cprint(f"\nSolved! {state.guesses} guess(es)", "green")
            return state.guesses
        else:
            player.update_state(result)
        print("")


def browser_game(
    variant="wordle",
    headless=False,
    theme="default",
    initial_guesses=[],
    player_type="bot",
):
    state = None
    try:
        logging.info("Visiting game site.")
        game_class = WordleGame if variant == "wordle" else AbsurdleGame
        state = game_class(headless=headless)
        player = init_player(state, player_type)

        result = None
        n_guesses = 0

        while True:
            logging.info("Selecting a word...")
            if initial_guesses:
                guess = initial_guesses.pop(0)
            else:
                guess = player.guess(state, prev=result)

            if not guess:
                print([letter_obj.value for letter_obj in result.letters])
                raise Exception("Could not find a word!")

            guess_for_print = colored(guess, "yellow", attrs=["bold", "underline"])
            logging.info(f"Guess #{n_guesses + 1} is {guess_for_print}")

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
        if state:
            state.quit()


def main():
    f = Figlet(font="roman")
    cprint("\n" + f.renderText("Wordle"), "cyan")

    parser = argparse.ArgumentParser(
        description="Play wordle on the command line or in a browser."
    )
    parser.add_argument(
        "-g",
        "--game",
        type=str,
        required=False,
        default="browser",
        help="Game type (browser or cli)",
    )
    parser.add_argument(
        "-p",
        "--player",
        type=str,
        required=False,
        default="human",
        help="Type of player (human, bot, or llm)",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run without visible browser (only for bot/llm players)"
    )
    parser.add_argument(
        "-v",
        "--variant",
        type=str,
        required=False,
        default="wordle",
        help="Game variant (wordle or absurdle)",
    )
    parser.add_argument(
        "-i",
        "--input-guesses",
        type=str,
        required=False,
        default=None,
        help="Comma-separated list of initial guesses (only for bot/llm players).",
    )
    parser.add_argument(
        "-t",
        "--theme",
        type=str,
        required=False,
        default="default",
        help=f"""Theme for progress output (only for bot/llm players).
            (Options: {','.join(VALID_THEMES)})"""
    )

    args = parser.parse_args()

    if args.game not in ("browser", "cli"):
        raise Exception(f"Invalid game type: {args.game}")

    if args.player not in ("human", "bot", "llm"):
        raise Exception(f"Invalid player {args.player}")

    if args.variant not in ("wordle", "absurdle"):
        raise Exception(f"Invalid variant: {args.variant}")

    if args.theme not in VALID_THEMES:
        raise Exception(f"Invalid theme: {args.theme}")

    initial_guesses = []
    if args.input_guesses:
        if re.match(r"[a-zA-Z]{5}(,[a-zA-Z]{5})*", args.input_guesses):
            initial_guesses = args.input_guesses.upper().split(",")
        else:
            raise Exception("Invalid guesses!")

    if args.player == "human" and args.headless:
        raise Exception("Cannot run headless human game")

    if args.game == "cli":
        console_game(
            player_type=args.player,
            initial_guesses=initial_guesses,
            theme=args.theme
        )
    elif args.game == "browser":
        browser_game(
            variant=args.variant,
            headless=args.headless,
            initial_guesses=initial_guesses,
            theme=args.theme,
            player_type=args.player,
        )


if __name__ == "__main__":
    main()
