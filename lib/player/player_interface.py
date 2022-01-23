class PlayerInterface:
    def guess(self, game_state, prev=None) -> str:
        pass

    def update_state(self, result) -> None:
        pass
