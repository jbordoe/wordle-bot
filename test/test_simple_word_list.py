import unittest

from lib.words.simple_word_list import SimpleWordList


class TestSimpleWordList(unittest.TestCase):
    def test_init(self):
        words = "foo bar baz".split()
        wl = SimpleWordList(words)
        self.assertIsInstance(wl, SimpleWordList)

    def test_find_words(self):
        words = "foo bar baz qux bat bob jib".split()
        wl = SimpleWordList(words)

        matches = wl.find_words(placed_letters=["b", None, None])

        self.assertEqual(
            matches, ["bar", "baz", "bat", "bob"], msg="lookup with placed"
        )

        matches = wl.find_words(excludes=[{"b"}, set(), set()], contains={"b"})
        self.assertEqual(matches, ["jib"], msg="lookup with contains, excludes")

        matches = wl.find_words(contains={"b"}, filter={"a"})
        self.assertEqual(matches, ["bob", "jib"], msg="lookup with contains, filter")

    def test_find_words_adv(self):
        words = """
            COTTE DELET
        """.replace("\n", "").split()
        wl = SimpleWordList(words)

        matches = wl.find_words(
            placed_letters=["", "O", "", "", "E"],
            contains={"E", "T", "O"},
            filter={"L", "R", "H", "D"},
            excludes=[{"O"}, {"E"}, set(), {"E"}, {"T"}],
        )
        self.assertEqual(set(matches), {"COTTE"}, msg="complex lookup")

        words = """
            SWAGE STAKE SPADE
        """.replace("\n", "").split()
        wl = SimpleWordList(words)

        matches = wl.find_words(
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


if __name__ == "__main__":
    unittest.main()
