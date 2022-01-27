class GameGuessResult:
    def __init__(self, guess, letters=None, correct=False, text=''):
        self.guess = guess
        self.letters = letters or [None for _ in range(len(guess))]
        self.correct = correct
        self.text = text or ''
