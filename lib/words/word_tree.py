from lib.words.word_set_interface import WordSetInterface

class WordTree(WordSetInterface):
    def __init__(self, word_collection):
        self.words = word_collection

    def find_words(
        self,
        placed_letters=None,
        contains=None,
        filter=None,
        excludes=None
    ):
        pass
