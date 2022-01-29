import sys
from lib.player.player_interface import PlayerInterface

class HumanPlayer(PlayerInterface):
    def guess(self, game_state, prev=None) -> str:
        prompt = "Enter your guess: "
        while True:
            print(prompt, end='')
            guess = input().strip().upper()
            if not guess in game_state.wordlist:
                sys.stdout.write("\033[F")
                print("\r" + " " * (len(guess) + len(prompt)) + "\r", end='')
                prompt = "\rNot Valid, try again: "
            else:
                sys.stdout.write("\033[F")
                print("\r" + " " * (len(guess) + len(prompt)) + "\r", end='')
                return guess.upper()

    def update_state(self, result) -> None:
        pass
