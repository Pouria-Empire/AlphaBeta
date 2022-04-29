class Player:
    def __init__(self, player_number, board):
        self.player_number = player_number
        self.opponent_number = 0
        if self.player_number == 0:
            self.opponent_number = 1
        self.board = board

    def get_next_move(self):
        # This defaults to a greedy player.
        res_coordinates = (0, 0)
        res_count = 0
        for i in range(self.board.get_n()):
            for j in range(self.board.get_n()):
                self.board.start_imagination()
                count = self.board.imagine_placing_piece(self.player_number, i, j)
                if count > res_count:
                    res_coordinates = (i, j)
                    res_count = count
        return res_coordinates
