class SudokuSolver:
    def __init__(self):
        self.solution_list = []

    def solve(self, board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for i in range(10):
                        if self.check_guess(board, row, col, i):
                            board[row][col] = i
                            if self.solve(board):
                                return True
                            else:
                                board[row][col] = 0
                    return False
        return True

    def count_solutions(self, board):
        self.solution_list = []

        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for i in range(1, 10):
                        if self.check_guess(board, row, col, i):
                            board[row][col] = i
                            if self.is_filled(board):
                                self.solution_list.append(board)
                            else:
                                self.count_solutions(board)
                        board[row][col] = 0
                    return

    def check_guess(self, board, row, col, val):
        return self.check_row(board, row, val) and self.check_col(board, col, val) and self.check_square(board, row, col, val)
    
    def check_row(self, board, row, val):
        return val not in board[row]
        
    def check_col(self, board, col, val):
        for i in range(9):
            if board[i][col] == val:
                return False
        return True
            
    def check_square(self, board, row, col, val):
        row_start = row//3 * 3
        col_start = col//3 * 3
        for i in range(3):
            for j in range(3):
                if board[row_start+i][col_start+j] == val:
                    return False
        return True

    def is_filled(self, board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    return False
        return True
    
    def print_board(self, board):
        disp = ""
        for i in range(9):
            for j in range(9):
                entry = board[i][j]
                if entry == 0:
                    entry = " "
                if j == 2 or j == 5:
                    disp += f"{entry} | "
                else:
                    disp += f"{entry}   "
            disp += "\n"
            if i == 2 or i == 5:
                disp += "- - - - - - - - - - - - - - - - -\n"
        print(disp)
