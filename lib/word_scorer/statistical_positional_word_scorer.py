import random

from lib.word_scorer.word_scorer_interface import WordScorerInterface

class StatisticalPositionalWordScorer(WordScorerInterface):
    AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self, wordlist, b=0):
        self.wordlist = list(wordlist)
        self.b = b
        self.update(wordlist)

    def rank(self, words):
        self.update(words)

        pairs = [(w, self.scores[w] + (random.random()*self.b)) for w in words]
        ranked = [pair[0] for pair in sorted(pairs, key=lambda x: x[1], reverse=True)]
        return ranked

    def update(self, wordlist):
        self.wordlist = list(wordlist)

        s = self._calculate_scores()
        self.scores = s
        None

    def _calculate_scores(self):
        
        freq = dict([(c, 0) for c in self.AZ])
        pfreq = dict([((i,c), 0) for i in range(5) for c in self.AZ])

        for w in self.wordlist:
            for i, l in enumerate(w):
                freq[l] += 1
                pfreq[(i,l)] += 1

        n = len(self.wordlist)

        scores = {}

        for c in self.AZ:
            freq[c] /= n
            for i in range(5): pfreq[(i,c)] /= n

        for w in self.wordlist:
            score = 0
            for i, l in enumerate(w):
                s = freq[l]
                ps = pfreq[(i,l)]
                
                score += s * ps
        
            scores[w] = score
            

        return scores