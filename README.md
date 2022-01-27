# wordle-bot

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

This will open a browser and play on the wordle site. 
```bash
python play_in_browser.py
```

### Command-line game
```bash
python wordle.py
```

## Tests
```bash
python -m unittest
```
