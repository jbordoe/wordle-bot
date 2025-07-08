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

#### In-Browser Play

Have the bot play a game of Wordle in a browser:
```bash
python play.py --variant wordle
```

Play Wordle in a browser, with `SALET` and `UNFIT` as the first guesses:
```bash
python play.py --variant wordle --guesses SALET,UNFIT
```

Have the bot play a game of [Absurdle](https://qntm.org/wordle) in a headless browser:
```bash
python play.py --variant absurdle --headless
```

Use `--help` for more information.

#### Command-Line Game

To play a game of Wordle on the command line yourself:
```bash
python wordle.py
```

### 3. Running Tests

To run the test suite:
```bash
python -m unittest
```