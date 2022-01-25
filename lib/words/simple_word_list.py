from lib.words.word_set_interface import WordSetInterface

class SimpleWordList(WordSetInterface):
    def __init__(self, word_collection):
        # TODO: add validation
        # e.g for now all words should have same length
        words = []
        for w in word_collection:
            data = {
                'str': w,
                'set': set(w)
                }
            words.append(data)
        self.words = words
        self.list = list(word_collection)

        self.len = len(list(word_collection)[0])

    def find_words(
        self,
        placed_letters=None,
        contains=set(),
        filter=set(),
        excludes=None
    ):

        placed = placed_letters or ['' for _ in range(self.len)]
        excludes = excludes or [set() for _ in range(self.len)]
        matches = []

        for w in self.words:
            invalid = False
            if w['set'].intersection(filter): continue
            for i, w_i in enumerate(w['str']):
                if placed[i] and placed[i] != w_i: invalid = True
                if w_i in excludes[i]: invalid = True
                if invalid: break
            if invalid or not w['set'].issuperset(contains): continue

            matches.append(w['str'])
        return matches
