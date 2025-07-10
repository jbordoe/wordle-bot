import logging
import random
import sys

from lib.word_scorer.word_scorer_interface import WordScorerInterface


class StatisticalPositionalWordScorer(WordScorerInterface):
    AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self, wordlist, b=0):
        """
        Parameters:
            wordlist (list):
                A list of words to analyze for scoring.
            b (int, optional):
                Determines the weight of randomness in the scoring algorithm.
                Default is 0
        """
        self.b = b
        self.update(wordlist)

    def rank(self, words):
        """Returns a list of words ranked by statistical score.
        Uses letter frequency and position frequency to calculate the score.

            Parameters:
                words (list): A list of words to rank.

            Returns:
                list: A list of words ranked by statistical score.
        """
        self.update(words)

        pairs = [(w, self.scores[w] + (random.random() * self.b)) for w in words]
        logging.debug(
            f"StatPosWordScorer.{sys._getframe().f_code.co_name}: pairs = {pairs}"
        )
        ranked = [pair[0] for pair in sorted(pairs, key=lambda x: x[1], reverse=True)]
        return ranked

    def update(self, wordlist):
        """Updates the internal wordlist with new words and recalculates scores.

        Parameters:
            wordlist (list[string]): List of words to update internal wordlist with.
        """
        self.wordlist = list(wordlist)

        self._calculate_scores()
        None

    def _calculate_scores(self):
        # stores frequency of each letter in the wordlist
        freq = dict([(c, 0) for c in self.AZ])
        # stores frequency of each letter in each position in the wordlist
        pfreq = dict([((i, c), 0) for i in range(5) for c in self.AZ])

        for w in self.wordlist:
            for i, letter in enumerate(w.upper()):
                freq[letter] += 1
                pfreq[(i, letter)] += 1

        n = len(self.wordlist)

        scores = {}

        for c in self.AZ:
            freq[c] /= n
            for i in range(5):
                pfreq[(i, c)] /= n

        for w in self.wordlist:
            score = 0
            for i, letter in enumerate(w.upper()):
                s = freq[letter]
                ps = pfreq[(i, letter)]

                score += s * ps

            scores[w] = score

        self.scores = scores
