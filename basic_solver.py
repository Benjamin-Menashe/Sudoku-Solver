# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 10:11:28 2021

@author: Benjamin
"""

# SUDOKU SOLVER
# for now just normal rules. Want to add:
    # diagonals
    # thermos (including >)
    # palindromes
    # knight
    # king
    # queen 9's
    # odds / evens
    # local min / max
    # killer (including unknown sum)
    # little killer
    # arrow
    # X-sums
    # sandwich
    # skyscraper
    # between lines
    # kropki (black dot 1:2, white dot consecutive)
    # no consecutives
    # circles
    # magic square (any size / orientation)
    # hidden duplicate
 
# also want to add GUI for input the sudoku problem instead of typing


# %% Get sudoku

board_blank = [
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0]
    ]

board_evil = [
    [1,0,0,4,0,0,6,0,0],
    [0,2,0,0,5,0,0,9,0],
    [0,0,3,0,0,6,0,0,8],
    [7,0,0,1,0,0,9,0,0],
    [0,9,0,0,2,0,0,4,0],
    [0,0,4,0,0,3,0,0,5],
    [5,0,0,8,0,0,2,0,0],
    [0,8,0,0,7,0,0,3,0],
    [0,0,7,0,0,9,0,0,1]
    ]

# %% To show the board nicely
def print_board(bo):
    
    for i in range(len(bo)): # over rows
        if i % 3 == 0 and i !=0:
            print('---------------------')
            
        for j in range(len(bo[0])): # over cols
            if j % 3 == 0 and j !=0:
                print('| ', end="")
                
            if  j == 8: # end of row
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end = "")
                
# %% Functions for solving

def find_empty(bo):
    for i in range(9):
        for j in range(9):
            if bo[i][j] == 0:
                return (i,j) # row, col
    return None # board is solved
            
            
def valid_normal(bo, num, pos):
    
    # check row
    for j in range(len(bo[0])):
        if bo[pos[0]][j] == num and pos[1] != j:
            return False
        
    # check col
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False
            
    # check square
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x*3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False
            
    return True


def solve(bo): # solve normal for now, will change
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find
        
    for i in range(1,10):
        if valid_normal(bo, i, (row,col)):
            bo[row][col] = i
            
            if solve(bo): # recursion
                return True
            
            bo[row][col] = 0 # reset
            
    return False
 

print('The problem is:')    
print_board(board_evil)
print('\n')
print('and the solution is:')
a = solve(board_evil)
if a:
    print_board(board_evil)
else:
    print('There is no solution!')