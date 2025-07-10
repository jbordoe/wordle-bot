import unittest

from lib.words.word_index import WordIndex


class TestWordIndex(unittest.TestCase):
    def test_init(self):
        words = "FOO BAR BAZ".split()
        index = WordIndex(words)
        self.assertIsInstance(index, WordIndex)

    def test_find_words(self):
        words = "FOO BAR BAZ QUX BAT BOB JIB".split()
        index = WordIndex(words)

        matches = index.find_words(placed_letters=["b", None, None])

        self.assertEqual(
            set(matches), {"BAR", "BAZ", "BAT", "BOB"}, msg="lookup with placed"
        )

        matches = index.find_words(excludes=[{"b"}, set(), set()], contains={"b"})
        self.assertEqual(set(matches), {"JIB"}, msg="lookup with contains, excludes")

        matches = index.find_words(contains={"b"}, filter={"a"})
        self.assertEqual(
            set(matches), {"BOB", "JIB"}, msg="lookup with contains, filter"
        )

    def test_find_words_adv(self):
        words = """
            COTTE DELET
        """.replace("\n", "").split()
        index = WordIndex(words)

        matches = index.find_words(
            placed_letters=["", "O", "", "", "E"],
            contains={"E", "T", "O"},
            filter={"L", "R", "H", "D"},
            excludes=[{"O"}, {"E"}, set(), {"E"}, {"T"}],
        )
        self.assertEqual(set(matches), {"COTTE"}, msg="complex lookup")

        words = """
            SWAGE STAKE SPADE
        """.replace("\n", "").split()
        index = WordIndex(words)

        matches = index.find_words(
            placed_letters=["S", "", "A", "", "E"],
            contains=set(),
            filter={
                "P",
                "N",
                "C",
                "H",
                "R",
                "L",
                "V",
                "U",
                "M",
                "I",
                "K",
                "D",
                "O",
                "T",
            },
            excludes=[set(), {"E"}, {"E", "S"}, {"E"}, set()],
        )
        self.assertEqual(set(matches), {"SWAGE"}, msg="complex lookup")

        words = """
            CADET JAYET CARET CATER WATER TAPER TAXER
        """.replace("\n", "").split()
        index = WordIndex(words)

        matches = index.find_words(
            placed_letters=["", "A", "", "E", "R"],
            contains={"T"},
            filter={"N", "L", "B", "M", "S"},
            excludes=[{"A"}, {"T"}, {"E", "T"}, set(), {"A", "T"}],
        )
        self.assertEqual(set(matches), {"TAPER", "TAXER"}, msg="complex lookup")


if __name__ == "__main__":
    unittest.main()
