# Wordle Bot

![](https://github.com/jbordoe/wordle-bot/blob/main/docs/wordlebot_50.png?raw=true)

A bot that plays Wordle.

[![CI Status](https://github.com/jbordoe/wordle-bot/actions/workflows/ci.yml/badge.svg)](https://github.com/jbordoe/wordle-bot/actions/workflows/ci.yml)
[![Code Coverage](https://img.shields.io/badge/coverage-N%25-orange)](https://github.com/jbordoe/wordle-bot/htmlcov/index.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


Designed to play Wordle and its variants, featuring multiple player types including human, statistical bot, and LLM-powered AI, with both command-line and in-browser play.

## Features

*   **Multiple Game Modes**: Supports the classic [Wordle](https://www.nytimes.com/games/wordle/index.html) and the more challenging [Absurdle](https://qntm.org/wordle).
*   **Player Types**:
    *   **Human Player**: Interactive command-line interface for manual play.
    *   **Statistical Bot**: An AI player that uses letter frequency analysis and statistical methods to make optimal guesses.
    *   **LLM Player**: Uses an LLM to generate intelligent guesses.
*   **In-Browser Automation**: Can simulate human interaction in a web browser.
*   **Headless Browser Support**: Run browser-based games in the background.
*   **Performance Evaluation**: Includes scripts to run extensive game simulations and generate performance statistics and visualizations for analysis.

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

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

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
