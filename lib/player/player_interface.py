class PlayerInterface:
    def guess(self, game_state, prev=None) -> str:
        raise NotImplementedError

    def update_state(self, result) -> None:
        raise NotImplementedError
