## Specially thanks to:
# https://github.com/yuxuan006/Othello/blob/ac33536bc35c7e50da93aab937e3dfee5c258a7f/yuchai.py#L148
# https://github.com/rohanp/othello/blob/master/othello.py
# Fakhredin Abdi
import copy
from random import shuffle
from player import Player
import game



INFINITY = 1000000000

gradingStrategy = [
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0, 100, -10,  10,   3,   3,  10, -10, 100,   0,
    0, -10, -20,  -3,  -3,  -3,  -3, -20, -10,   0,
    0,  10,  -3,   8,   1,   1,   8,  -3,  10,   0,
    0,   3,  -3,   1,   1,   1,   1,  -3,   3,   0,
    0,   3,  -3,   1,   1,   1,   1,  -3,   3,   0,
    0,  10,  -3,   8,   1,   1,   8,  -3,  10,   0,
    0, -10, -20,  -3,  -3,  -3,  -3, -20, -10,   0,
    0, 100, -10,  10,   3,   3,  10, -10, 100,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
]


class AlphaBetaPlayer(Player):
    def __init__(self, player_number, board):
        self.resBlack = 0
        self.resWhite = 0
        super().__init__(player_number, board)

    def updateTheFourCorners(self):
    #---1B. Modify upper-left corner cell's values if the HUMAN has taken that corner.
        M = self.board.imaginary_board_grid
        if M[0][0] == 1:
            gradingStrategy[12] = -50
            gradingStrategy[21] = -200
            gradingStrategy[22] = -50

    #---2B. Modify upper-right corner cell's values if the HUMAN has taken that corner.
        if M[0][7] == 1:
            gradingStrategy[17] = -50
            gradingStrategy[28] = -200
            gradingStrategy[27] = -50

    #---3B. Modify lower-left corner cell's values if the HUMAN has taken that corner.
        if M[7][0] == 1:
            gradingStrategy[71] = -50
            gradingStrategy[72] = -200
            gradingStrategy[82] = -50

    #---4B. Modify lower-right corner cell's values if the HUMAN has taken that corner.
        if M[7][7] == 1:
            gradingStrategy[87] = -50
            gradingStrategy[78] = -200
            gradingStrategy[77] = -50
    #---1W. Modify upper-left corner cell's values if the COMPUTER has taken that corner.
        if M[0][0] == 0:
            gradingStrategy[12] = 100
            gradingStrategy[21] = 100
            gradingStrategy[22] = 100
    #---2W. Modify upper-right corner cell's values if the COMPUTER has taken that corner.
        if M[0][7] == 0:
            gradingStrategy[17] = 100
            gradingStrategy[28] = 100
            gradingStrategy[27] = 100
    #---3W. Modify lower-left corner cell's values if the COMPUTER has taken that corner.
        if M[7][0] == 0:
            gradingStrategy[71] = 100
            gradingStrategy[72] = 100
            gradingStrategy[82] = 100
    #---4W. Modify lower-right corner cell's values if the COMPUTER has taken that corner.
        if M[7][7] == -1:
            gradingStrategy[87] = 100
            gradingStrategy[78] = 100
            gradingStrategy[77] = 100



    def eval_fn(self, color,count):
        
        # if color:
        #     if count < self.resWhite:
        #         return -INFINITY
        #     self.resWhite = count
        # else:
        #     if count < self.resBlack:
        #         return INFINITY
        #     self.resBlack = count

        point_black = 0
        point_white = 0
        for row in range(8):
            for cell in range(8):
                if self.board.imaginary_board_grid[row][cell] == 0:
                    point_black += 1
                elif self.board.imaginary_board_grid[row][cell] == 1:
                    point_white +=1

        diff_points = (point_white - point_black)*100
        point = 0

        # #The color of the opponent
        # opp = 1
        if color == 0:
            color = 1
            opp = 0
        else:
            color = 1
            opp = 0

        for row in range(8):
            for col in range(8):
                #calculate the point of current player
                if self.board.imaginary_board_grid[row][col] == color:
                    point += gradingStrategy[(row+1)*10+1+col]
                #calculate the point of the opponent
                elif self.board.imaginary_board_grid[row][col] == opp:
                    point -= gradingStrategy[(row+1)*10+1+col]
        return point+diff_points

    def alpha_beta(self, color, depth, alpha, beta,count):
        if depth == 0:
            return self.eval_fn(color,count)
        # if gamePlay.gameOver(board):
        #     return gamePlay.score(board)

        moves = []
        for row in range(8):
            for col in range(8):
                if self.board.is_imaginary_move_valid(color, row, col):
                    moves.append((row, col))

        #shuffle the moves may be needed for hanging place in every game
        shuffle(moves)

        if len(moves) == 0:
            return None
        if moves == None:
            return self.eval_fn(color,count)

        opp = 1
        if color == 1:
            opp = 0

        # try each move
        #evaluate max's position and choose the best value
        if color == 1:
            copy_board = copy.deepcopy(self.board.imaginary_board_grid)
            for move in moves:
                counts = self.board.imagine_placing_piece(color, move[0],move[1])
                #cut off the branches
                bes = self.alpha_beta(opp, depth-1, alpha, beta,counts)
                if bes == None:
                    continue

                alpha = max(alpha, bes)

                self.board.imaginary_board_grid = copy.deepcopy(copy_board)
                if beta <= alpha:
                    return None


            return alpha

        #evaluate min's position and choose the best value
        if color == 0:
            copy_board = copy.deepcopy(self.board.imaginary_board_grid)
            for move in moves:
                # newBoard = self.board.__board_grid[:]
                counts = self.board.imagine_placing_piece(color, move[0],move[1])
                #cut off the branches
                bes = self.alpha_beta(opp, depth-1, alpha, beta,counts)
                if bes == None:
                    continue

                # bes = min(bes,counts)
                self.board.imaginary_board_grid = copy.deepcopy(copy_board)
                beta = min(beta, bes)

                if beta <= alpha:
                    return None

                
            return beta

    def get_next_move(self):
        best_val = None
        best_move = None
        moves = []

        color = 1 # assume we are white
        self.board.start_imagination()
        for row in range(8):
            for col in range(8):
                # if gamePlay.valid(board, color, (row, col)):
                if self.board.is_move_valid(color, row, col):
                    moves.append((row, col))

        # for change start point
        shuffle(moves)

        if len(moves) == 0:
            return None
        if moves == None:
            return None

        opp = 1
        if color == 1:
            opp = 0
        #evaluate max's position and choose the best value
        if color == 1:
            best_val = -INFINITY
            copy_board = copy.deepcopy(self.board.imaginary_board_grid)
            for move in moves:
                # newBoard = self.board.__board_grid[:]
                counts = self.board.imagine_placing_piece(color, move[0],move[1])
                alpha = - INFINITY 
                beta = INFINITY
                #we want to choose the max one
                best = self.alpha_beta(opp, 3, alpha, beta,0)

                self.board.imaginary_board_grid = copy.deepcopy(copy_board)
                if best==None:
                    continue

                # best = max(best,counts)
                #update best move
                if best_val < best:
                    best_val = best
                    best_move = move

        #evaluate min's position and choose the best value
        if color == 0:
            best_val = INFINITY
            copy_board = copy.deepcopy(self.board.imaginary_board_grid)
            for move in moves:
                # newBoard = self.board.__board_grid[:]
                counts = self.board.imagine_placing_piece(color, move[0],move[1])
                alpha = - INFINITY 
                beta = INFINITY
                #we want to choose the min one
                best = self.alpha_beta(opp, 3, alpha, beta,0)

                self.board.imaginary_board_grid = copy.deepcopy(copy_board)
                if best == None:
                    continue

                # best = min(best,counts)
                #update best move
                if best_val > best:
                    best_val = best
                    best_move = move
                
        return best_move