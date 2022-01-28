import random

from lib.ranker_interface import RankerInterface

class RandomRanker(RankerInterface):
    AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self, wordlist):
        self.wordlist = list(wordlist)

    def rank(self, words):
        w = list(words)
        return random.sample(w, 1) + w

    def update(self, wordlist):
        self.wordlist = list(wordlist)
