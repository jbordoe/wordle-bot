import unittest

from lib.game.game_interface import GameInterface


class TestGameInterface(unittest.TestCase):
    def setUp(self):
        """
        Set up a minimal mock sublass for each test.
        """

        class TestGame(GameInterface):
            def __init__(self):
                pass

        self.subclass = TestGame()

    def test_init_raises_not_implemented(self):
        """
        Tests that instantiating GameInterface directly raises NotImplementedError.
        """
        with self.assertRaises(NotImplementedError):
            GameInterface()

    def test_update_raises_not_implemented(self):
        """
        Tests that calling the 'update' method on a subclass that hasn't
        implemented it raises NotImplementedError.
        """
        with self.assertRaises(NotImplementedError):
            self.subclass.update("test")

    def test_undo_raises_not_implemented(self):
        """
        Tests that calling the 'undo' method on a subclass that hasn't
        implemented it raises NotImplementedError.
        """
        with self.assertRaises(NotImplementedError):
            self.subclass.undo()

    def test_quit_raises_not_implemented(self):
        """
        Tests that calling the 'quit' method on a subclass that hasn't
        implemented it raises NotImplementedError.
        """

        class TestGame(GameInterface):
            def __init__(self):
                pass

        game = TestGame()
        with self.assertRaises(NotImplementedError):
            game.quit()


if __name__ == "__main__":
    unittest.main()
