import logging

from lib.words.word_set_interface import WordSetInterface


class WordIndex(WordSetInterface):
    AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self, word_collection):
        wordlen = len(list(word_collection)[0])
        ordered_index = [{} for _ in range(wordlen)]
        unordered_index = dict([(c, set()) for c in self.AZ])

        for c in self.AZ:
            for i in range(wordlen):
                ordered_index[i][c] = set()

        for w in word_collection:
            wup = w.upper()
            for c in set(wup):
                unordered_index[c].add(wup)
            for i, c in enumerate(wup):
                ordered_index[i][c].add(wup)

        self.ordered_index = ordered_index
        self.unordered_index = unordered_index
        self.wordset = set(word_collection)
        self.list = list(word_collection)

    # note: function documentation below in standard format
    def find_words(self, placed_letters=[], contains=None, filter=set(), excludes=[]):
        """
        Finds words that match the given constraints.

        Parameters:
        placed_letters (list): List of letters already placed in the word.
            Unknown letters are represented by falsey values.
        contains (list): Letters present in the word, but not necessarily placed.
        filter (set): Set of letters that must not be present in the word.
        excludes (list[set]): Letters that can't be present in each respective position.

        Returns:
        list: List of words that match the given constraints.
        """
        logging.debug(f"""
        placed_letters={placed_letters},
        contains={contains},
        filter={filter},
        excludes={excludes}
        """)
        # ensure all letters are upper case
        placed_letters = [
            letter.upper() if letter else None for letter in placed_letters
        ]
        contains = [letter.upper() for letter in contains] if contains else None
        filter = set([letter.upper() for letter in filter])
        excludes = [
            set([letter.upper() for letter in group]) for group in excludes
        ]

        placed_pairs = [c for c in enumerate(placed_letters) if c[1]]
        placed_set = self._find_in_ordered(placed_pairs)

        contains_set = self._find_in_unordered(contains) if contains else None
        filter_set = set().union(
            *[self.unordered_index[letter.upper()] for letter in filter]
        )

        filter_set = filter_set.union(
            *[
                self.ordered_index[i][letter]
                for i, ex in enumerate(excludes)
                if ex
                for letter in ex
            ]
        )

        result = self.wordset
        if placed_set is not None:
            result = result.intersection(placed_set)
        if contains_set is not None:
            result = result.intersection(contains_set)
        if filter_set is not None:
            result = result.difference(filter_set)

        return list(result)

    def _find_in_ordered(self, letters_with_index):
        if not letters_with_index:
            return self.wordset

        sets = [self.ordered_index[i][letter] for i, letter in letters_with_index]
        result = sets[0].intersection(*sets[1:])
        return result

    def _find_in_unordered(self, letters):
        if not letters:
            return self.wordset

        sets = [self.unordered_index[letter] for letter in letters]
        result = sets[0].intersection(*sets[1:])
        return result
