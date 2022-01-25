import unittest

from lib.words.simple_word_list import SimpleWordList

class TestSimpleWordList(unittest.TestCase):
    def test_init(self):
        words = 'foo bar baz'.split()
        wl = SimpleWordList(words)
        self.assertIsInstance(wl, SimpleWordList)

    def test_find_words(self):
        words = 'foo bar baz qux bat bob jib'.split()
        wl = SimpleWordList(words)

        matches = wl.find_words(
            placed_letters=['b', None, None]
        )

        self.assertEqual(
            matches,
            ['bar', 'baz', 'bat', 'bob'],
            msg='lookup with placed'
        )

        matches = wl.find_words(
            excludes=[{'b'}, set(), set()],
            contains={'b'}
        )
        self.assertEqual(
            matches,
            ['jib'],
            msg='lookup with contains, excludes'
        )

        matches = wl.find_words(
            contains={'b'},
            filter={'a'}
        )
        self.assertEqual(
            matches,
            ['bob', 'jib'],
            msg='lookup with contains, filter'
        )

if __name__ == "__main__":
    unittest.main()
