from lib.player.player_interface import PlayerInterface

class HumanPlayer(PlayerInterface):
    def guess(self, game_state, prev=None) -> str:
        while True:
            print("""
Enter your guess! Must be a {}-letter word
    """.format(game_state.word_length))
            guess = input().strip().upper()
            if not guess in game_state.wordlist:
                print("Your guess is not valid")
            else:
                return guess

    def update_state(self, result) -> None:
        pass
