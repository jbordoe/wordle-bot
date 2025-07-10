class GameGuessResult:
    def __init__(self, guess, letters=None, correct=False, text="", valid=True):
        """
        Represents the result of a guess

            Parameters:
                guess (str): The guessed word
                letters (list): A list of tuples of the form (letter, state)
                    where state corresponds to one of the GameInterface constants
                correct (bool): Whether the guess was correct
                text (str): Any additional text to display
                valid (bool): Whether the guess is valid
        """
        self.guess = guess
        # TODO: change from a list of tuples to a list of GameGuessLetter objects
        self.letters = letters or [None for _ in range(len(guess))]
        self.correct = correct
        self.text = text or ""
        self.valid = valid
