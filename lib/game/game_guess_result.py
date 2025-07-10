class GameGuessResult:
    def __init__(self, guess, letters=None, correct=False, text=''):
        """
        Represents the result of a guess

            Parameters:
                guess (str): The guessed word
                letters (list): A list of tuples of the form (letter, state)
                    where state corresponds to one of the GameInterface constants
                correct (bool): Whether the guess was correct
                text (str): Any additional text to display
        """
        self.guess = guess
        self.letters = letters or [None for _ in range(len(guess))]
        self.correct = correct
        self.text = text or ''
