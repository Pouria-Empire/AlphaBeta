import numpy as np

class Board:
    def __init__(self, n=8):
        self.__colors = ["black", "white"]
        self.__board_grid = np.full((n, n), -1)
        self.__n = n
        self.__board_grid[n // 2][n // 2] = 0
        self.__board_grid[n // 2 - 1][n // 2 - 1] = 0
        self.__board_grid[n // 2][n // 2 - 1] = 1
        self.__board_grid[n // 2 - 1][n // 2] = 1
        self.imaginary_board_grid = None

    def get_board_grid(self):
        ''' Return the 2D list representing the board.'''
        return np.copy(self.__board_grid)

    def get_n(self):
        ''' Return the dimension the board.'''
        return self.__n
    
    def get_color(self, i, j):
        ''' Given the coordinates (i, j) number, 
            return the color of the piece placed there.'''
        if self.__board_grid[i][j] not in [0, 1]:
            return None
        return self.__colors[self.__board_grid[i][j]]

    def is_move_valid(self, player_number, i, j):
        ''' Given the player number and a position (i, j),
            return True if the position is a valid move for the color. 
            return False otherwise.'''
        if i < 0 or j < 0 or i >= self.__n or j >= self.__n or self.__board_grid[i][j] != -1:
            return False
        for row_coeff in range(-1, 2):
            for column_coeff in range(-1, 2):
                k = 1
                row = i + row_coeff * k
                column = j + column_coeff * k
                is_valid = False
                while row >= 0 and row < self.__n and column >= 0 and column < self.__n and self.__board_grid[row][column] != -1:
                    if self.__board_grid[row][column] == player_number:
                        if is_valid:
                            return True
                        break
                    is_valid = True
                    k += 1
                    row = i + row_coeff * k
                    column = j + column_coeff * k
        return False

    def place_piece(self, player_number, i, j):
        ''' Given the player number, place a piece with its color in position (i, j).
            Upon success, return the count of overturned pieces plus one. Return 0 otherwise.'''
        if i < 0 or j < 0 or i >= self.__n or j >= self.__n or self.__board_grid[i][j] != -1:
            return 0
        all_turned_pieces = []
        for row_coeff in range(-1, 2):
            for column_coeff in range(-1, 2):
                k = 1
                row = i + row_coeff * k
                column = j + column_coeff * k
                turned_pieces = []
                while row >= 0 and row < self.__n and column >= 0 and column < self.__n and self.__board_grid[row][column] != -1:
                    if self.__board_grid[row][column] == player_number:
                        if turned_pieces:
                            all_turned_pieces.append(turned_pieces)
                        break
                    turned_pieces.append((row, column))
                    k += 1
                    row = i + row_coeff * k
                    column = j + column_coeff * k
        if all_turned_pieces == []:
            return 0
        self.__board_grid[i][j] = player_number
        count = 1
        for turned_pieces in all_turned_pieces:
            count += len(turned_pieces)
            for turned_piece in turned_pieces:
                self.__board_grid[turned_piece[0]][turned_piece[1]] = player_number
        return count

    def start_imagination(self):
        ''' Prepare a copy of the board to test moves without a real impact.'''
        self.imaginary_board_grid = np.copy(self.__board_grid)

    def is_imaginary_move_valid(self, player_number, i, j):
        ''' Given the player number and a position (i, j),
            return True if the position is a valid move for the color in the imaginary board. 
            return False otherwise.'''
        if i < 0 or j < 0 or i >= self.__n or j >= self.__n or self.imaginary_board_grid[i][j] != -1:
            return False
        for row_coeff in range(-1, 2):
            for column_coeff in range(-1, 2):
                k = 1
                row = i + row_coeff * k
                column = j + column_coeff * k
                is_valid = False
                while row >= 0 and row < self.__n and column >= 0 and column < self.__n and self.imaginary_board_grid[row][column] != -1:
                    if self.imaginary_board_grid[row][column] == player_number:
                        if is_valid:
                            return True
                        break
                    is_valid = True
                    k += 1
                    row = i + row_coeff * k
                    column = j + column_coeff * k
        return False

    def imagine_placing_piece(self, player_number, i, j):
        ''' Test moves on the copy board without a real impact.'''
        if i < 0 or j < 0 or i >= self.__n or j >= self.__n or self.imaginary_board_grid[i][j] != -1:
            return 0
        all_turned_pieces = []
        for row_coeff in range(-1, 2):
            for column_coeff in range(-1, 2):
                k = 1
                row = i + row_coeff * k
                column = j + column_coeff * k
                turned_pieces = []
                while row >= 0 and row < self.__n and column >= 0 and column < self.__n and self.imaginary_board_grid[row][column] != -1:
                    if self.imaginary_board_grid[row][column] == player_number:
                        if turned_pieces:
                            all_turned_pieces.append(turned_pieces)
                        break
                    turned_pieces.append((row, column))
                    k += 1
                    row = i + row_coeff * k
                    column = j + column_coeff * k
        if all_turned_pieces == []:
            return 0
        self.imaginary_board_grid[i][j] = player_number
        count = 1
        for turned_pieces in all_turned_pieces:
            count += len(turned_pieces)
            for turned_piece in turned_pieces:
                self.imaginary_board_grid[turned_piece[0]][turned_piece[1]] = player_number
        return count

    def get_scores(self):
        ''' Return the scores of the players in a list.
            The first number is the count of black pieces.
            The second number is the count of white pieces.'''
        scores = [0, 0]
        for row in self.__board_grid:
            for cell in row:
                if cell >= 0:
                    scores[cell] += 1
        return scores

    def __str__(self):
        s = []
        for row in self.__board_grid:
            s.append(" ".join(map(str, row)))
        return "\n".join(s)