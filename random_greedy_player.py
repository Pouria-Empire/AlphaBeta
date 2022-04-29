from player import Player
import random

class RandomGreedyPlayer(Player):
    def get_next_move(self):
        res_coordinates = []
        res_count = 0
        for i in range(self.board.get_n()):
            for j in range(self.board.get_n()):
                self.board.start_imagination()
                count = self.board.imagine_placing_piece(self.player_number, i, j)
                if count == res_count:
                    res_coordinates.append((i, j))
                if count > res_count:
                    res_coordinates = [(i, j)]
                    res_count = count
        return random.choice(res_coordinates)
