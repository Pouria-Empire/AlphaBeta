from board import Board
from player import Player
from random_player import RandomPlayer
from human_player import HumanPlayer
from random_greedy_player import RandomGreedyPlayer
# from alphabeta import AlphaBetaPlayer
import alphabeta
import visualizer

class Game:
    def __init__(self, first_player_class, second_player_class):
        self.first_player_class = first_player_class
        self.second_player_class = second_player_class

    def play(self, visualize=False):
        board = Board()
        black = self.first_player_class(0, board)
        white = self.second_player_class(1, board)
        done = False
        if visualize:
            visualizer.visualize_init(board)
        while not done:
            black_move = black.get_next_move()
            if black_move:
                black_moved = board.place_piece(0, *black_move)
                if visualize:
                    visualizer.visualize(board)
            else:
                black_moved = 0
            white_move = white.get_next_move()
            if white_move:
                white_moved = board.place_piece(1, *white_move)
                if visualize:
                    visualizer.visualize(board)
            else:
                white_moved = 0
            if not black_moved and not white_moved:
                done = True
        scores = self.get_scores(board.get_board_grid())
        return scores

    def get_scores(self, board_grid):
        scores = [0, 0]
        for row in board_grid:
            for cell in row:
                if cell >= 0:
                    scores[cell] += 1
        return scores

    def bulk_play(self, n):
        results = {'b': 0, 'w': 0, 'd': 0}
        for _ in range(n):
            result = self.get_winner(self.play())
            results[result] += 1
        return results

    def get_winner(self, scores):
        if scores[0] > scores[1]:
            return 'b'
        if scores[0] < scores[1]:
            return 'w'
        return 'd'

if __name__ == '__main__':
    # Time Limit for each game without graphics: ~60 seconds
    game = Game(Player, alphabeta.AlphaBetaPlayer)
    # game = Game(Player, RandomGreedyPlayer)
    # print(game.play(True))
    # game.bulk_play(100)
    print(game.bulk_play(20))