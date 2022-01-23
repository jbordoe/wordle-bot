class GameGuessResult:
    def __init__(self, guess, letters=None):
        self.guess = guess
        self.letters = letters or [None for _ in range(len(guess))]
