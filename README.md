# Wordle Bot

![](https://github.com/jbordoe/wordle-bot/blob/main/docs/wordlebot_50.png?raw=true)

A bot that plays [Wordle](https://www.powerlanguage.co.uk/wordle/)

## Features

*   **Multiple Game Modes**: Supports [Wordle](https://www.powerlanguage.co.uk/wordle/) as well as the more challenging [Absurdle](https://qntm.org/wordle).
*   **Configurable Bot Strategy**: The bot's guessing strategy can be swapped out. Currently includes:
    *   A statistical ranker that uses letter frequency to make guesses.
    *   A random ranker for baseline comparisons.
*   **In-Browser Automation**: The bot can play the game directly in a web browser.
*   **Headless Mode**
*   **Command-Line Interface**: An interactive command-line version of Wordle.
*   **Performance Evaluation**: Scripts are provided to run the bot through thousands of games and generate performance statistics and visualizations.

## Getting Started

This project uses [pipenv](https://pipenv.pypa.io/en/latest/) for dependency management.

### 1. Setup

Install Python packages:

```bash
pipenv install
```

Next, ensure that [`geckodriver`](https://github.com/mozilla/geckodriver) is installed and available in your system's PATH.

Finally, initialize virtual Python env:

```bash
pipenv shell
```

### 2. Running the Bot

`main.py` is the entry point for playing Wordle.

#### In-Browser Play (Bot/LLM)

Have the bot play a game of Wordle in a browser:
```bash
python main.py --player bot --variant wordle
```

Play Wordle in a browser, with `SALET` and `UNFIT` as the first guesses:
```bash
python main.py --player bot --variant wordle --guesses SALET,UNFIT
```

Have the bot play a game of [Absurdle](https://qntm.org/wordle) in a headless browser:
```bash
python main.py --player bot --variant absurdle --headless
```

Have the LLM play a game of Wordle in a browser:
```bash
python main.py --player llm --variant wordle
```

#### Command-Line Game (Human)

To play a game of Wordle on the command line yourself:
```bash
python main.py --player human
```

Use `--help` for more information on all available options.

### 3. Running Tests

To run the test suite:
```bash
python -m unittest discover test
```

#### Code Coverage

This project uses `coverage.py` to measure test coverage.

Run the tests and collect coverage data:
```bash
pipenv run coverage run -m unittest discover test
```

View the report in the terminal:
```bash
pipenv run coverage report -m
```

Generate a detailed HTML report:
```bash
pipenv run coverage html
```
The report will be saved in `htmlcov/index.html`.
