from lib.word_scorer.word_scorer_interface import WordScorerInterface


class RandomWordScorer(WordScorerInterface):
    AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self, wordlist):
        self.wordlist = list(wordlist)

    def rank(self, words):
        return sorted(list(words))

    def update(self, wordlist):
        self.wordlist = list(wordlist)
