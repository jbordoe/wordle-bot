import random

import requests


class WordLoader:
    WORDLE_VALID_GUESSES_URL = "https://gist.githubusercontent.com/cfreshman/cdcdf777450c5b5301e439061d29694c/raw/de1df631b45492e0974f7affe266ec36fed736eb/wordle-allowed-guesses.txt"
    WORDLE_ANSWERS_URL = "https://gist.githubusercontent.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b/raw/5d752e5f0702da315298a6bb5a771586d6ff445c/wordle-answers-alphabetical.txt"

    @classmethod
    def load_wordlist(cls, sample_size=None):
        w1 = requests.get(cls.WORDLE_VALID_GUESSES_URL).text.upper().split("\n")
        w2 = requests.get(cls.WORDLE_ANSWERS_URL).text.upper().split("\n")

        wl = list(set(w1).union(set(w2)))
        # Drop any empty strings
        wl = [w for w in wl if w]
        if sample_size:
            wl = random.sample(wl, sample_size)
        return wl
