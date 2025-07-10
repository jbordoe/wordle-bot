import unittest

from lib.player.player_interface import PlayerInterface


class TestPlayerInterface(unittest.TestCase):
    def test_guess_raises_not_implemented(self):
        player = PlayerInterface()
        with self.assertRaises(NotImplementedError):
            player.guess(None)

    def test_update_state_raises_not_implemented(self):
        player = PlayerInterface()
        with self.assertRaises(NotImplementedError):
            player.update_state(None)


if __name__ == "__main__":
    unittest.main()
