import logging

from functools import reduce

from lib.words.word_set_interface import WordSetInterface

class WordIndex(WordSetInterface):
    AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def __init__(self, word_collection):
        wordlen = len(list(word_collection)[0])
        ordered_index = [{} for _ in range(wordlen)]
        unordered_index = dict([(c, set()) for c in self.AZ])

        for c in self.AZ:
            for i in range(wordlen):
                ordered_index[i][c] = set()

        for w in word_collection:
            w = w.upper()
            for c in set(w):
                unordered_index[c].add(w)
            for i, c in enumerate(w):
                ordered_index[i][c].add(w)

        self.ordered_index = ordered_index
        self.unordered_index = unordered_index
        self.wordset = set(word_collection)
        self.list = list(word_collection)

    # TODO: add param to filter given words (i.e old guesses)
    def find_words(
        self,
        placed_letters=[],
        contains=None,
        filter=set(),
        excludes=[],
    ):
        logging.debug(f"""
        placed_letters={placed_letters},
        contains={contains},
        filter={filter},
        excludes={excludes}
        """)
        placed_pairs = [c for c in enumerate(placed_letters) if c[1]]
        placed_set = self._find_in_ordered(placed_pairs)

        contains_set = self._find_in_unordered(contains) if contains else None
        filter_set = set().union(*[self.unordered_index[l.upper()] for l in filter])
        
        filter_set = filter_set.union(
            *[self.ordered_index[i][l] for i, ex in enumerate(excludes) if ex for l in ex]
        )

        result = self.wordset
        if placed_set != None: result = result.intersection(placed_set)
        if contains_set != None: result = result.intersection(contains_set)
        if filter_set != None: result = result.difference(filter_set)
        #if excludes_set != None: result = result.difference(excludes_set)

        return list(result)
        
    def _find_in_ordered(self, letters_with_index):
        if not letters_with_index: return self.wordset

        sets = [self.ordered_index[i][l] for i,l in letters_with_index]
        result = sets[0].intersection(*sets[1:])
        return result

    def _find_in_unordered(self, letters):
        if not letters: return self.wordset

        sets = [self.unordered_index[l] for l in letters]
        result = sets[0].intersection(*sets[1:])
        return result
