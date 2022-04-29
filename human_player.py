from player import Player

class HumanPlayer(Player):
    def get_next_move(self):
        i, j = map(int, input().split())
        return (i, j)
