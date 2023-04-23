'''
SUDOKU GENERATOR

Objective:
- Create a program to generate a random valid 9x9 Sudoku puzzle with
  a unique solution

Approach:
- Generate a fully filled, valid Sudoku board
- Based on user-selected difficulty, remove K number of
  entries to complete the puzzle
- Have the option to solve the puzzle once generated

Brute Force Method:
The most obvious way to approach the initial problem of generating
the filled in board would be to simply iterate over each entry,
choosing a random value from 1-9 and checking if that value works,
moving on if it does, and backtracking when needed.

Optimization:
Note that for any 9x9 sudoku grid, the three diagonal 3x3 sections
of the grid are independent of each other within the rules of
Sudoku. 

For reference:
*  *  *  0  0  0  0  0  0 
*  *  *  0  0  0  0  0  0 
*  *  *  0  0  0  0  0  0 
0  0  0  *  *  *  0  0  0 
0  0  0  *  *  *  0  0  0 
0  0  0  *  *  *  0  0  0 
0  0  0  0  0  0  *  *  * 
0  0  0  0  0  0  *  *  * 
0  0  0  0  0  0  *  *  * 

Thus, if we start by filling in these three sections first, we don't
need to check the columns or rows when adding a new entry. Further,
since the rest of the board is determined by these three diagonal
sections, we can continue by simply solving the the board normally
without picking new entries randomly.

We will construct our algorithm accordingly.
'''

import random
from sudoku_solver import SudokuSolver

sdk = SudokuSolver()
create_board = True

while create_board:
    # initialize board
    board = []
    for i in range(9):
        row = []
        for j in range(9):
            row.append(0)
        board.append(row)

    # begin by filling in the diagonal 3x3 regions
    for i in range(3):
        row_start = col_start = i * 3
        for row in range(row_start, row_start+3):
            for col in range(col_start, col_start+3):
                values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                while True:
                    # choose random entry
                    val = random.choice(values)
                    # check for validity
                    if sdk.check_square(board, row, col, val):
                        board[row][col] = val
                        break
                    else:
                        values.remove(val)

    # now solve the rest of the board
    sdk.solve(board)

    # note: 64 is the maximum amount of empty entries a board can have and still be solvable
    difficulties = {'easy': 20, 'medium': 35, 'hard': 50, 'extreme': 64}
    # ask user for difficulty level
    user_in = input("What difficulty would you like the puzzle to be? (easy, medium, hard, extreme)\n-> ").lower()
    while True:
        try:
            thresh = difficulties[user_in]
            puzzle_difficulty = user_in
            break
        except KeyError:
            user_in = input("Please enter a valid difficulty\n-> ").lower()

    if user_in == 'extreme':
        print("\nNOTE: An 'extreme' difficulty puzzle may sometimes be slow to generate")

    indeces = [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),
            (1,0),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),
            (2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(2,6),(2,7),(2,8),
            (3,0),(3,1),(3,2),(3,3),(3,4),(3,5),(3,6),(3,7),(3,8),
            (4,0),(4,1),(4,2),(4,3),(4,4),(4,5),(4,6),(4,7),(4,8),
            (5,0),(5,1),(5,2),(5,3),(5,4),(5,5),(5,6),(5,7),(5,8),
            (6,0),(6,1),(6,2),(6,3),(6,4),(6,5),(6,6),(6,7),(6,8),
            (7,0),(7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,7),(7,8),
            (8,0),(8,1),(8,2),(8,3),(8,4),(8,5),(8,6),(8,7),(8,8)]
    
    # remove k entries from the board, where k <= thresh
    for k in range(thresh):
        try:
            while True:
                index = random.choice(indeces)
                row = index[0]
                col = index[1]
                old_val = board[row][col]
                board[row][col] = 0
                
                sdk.count_solutions(board)
                indeces.remove(index)
                # continue only if board is solvable and unique
                if len(sdk.solution_list) == 1:
                    break
                else:
                    board[row][col] = old_val
        except IndexError:
            # if we run out of entries to remove, finish
            break

    print(f"\nGenerated board with {k+1} missing entries:")
    sdk.print_board(board)

    user_in = input("Would you like to solve the puzzle? (Y/N)\n-> ").upper()
    if user_in == 'Y':
        sdk.solve(board)
        print("\nSolved board:")
        sdk.print_board(board)
    
    user_in = input("Would you like to generate another puzzle? (Y/N)\n-> ").upper()
    create_board = user_in == 'Y'
