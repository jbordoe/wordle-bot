# wordle-bot

![](https://github.com/jbordoe/wordle-bot/blob/main/docs/wordlebot_50.png?raw=true)

A bot that plays [wordle](https://www.powerlanguage.co.uk/wordle/)

## Setup

This project uses [pipenv](https://pipenv.pypa.io/en/latest/)

Install Python packages:

```bash
pipenv install
```

Ensure geckodriver is installed

Initialize virtual Python env:

```bash
pipenv shell
```

## Running

### In-browser play

Have the bot play a game of wordle in a browser
```bash
python play.py -v wordle
```

Play wordle in a browser, with `salet` and `unfit` as the first guesses 
```bash
python play.py -v wordle -g salet,unfit
```

Have the bot play a game of [absurdle](https://qntm.org/wordle) in a headless browser
```bash
python play.py -v absurdle --headless
```

use `--help` for more information

### Command-line game
```bash
python wordle.py
```

## Tests
```bash
python -m unittest
```

Test
