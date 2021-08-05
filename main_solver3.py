# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 20:11:54 2021

@author: Benjamin
"""

from puzzle import puzzle
from valids import *

sudoku = puzzle()
sudoku.board = [
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,4,0,0,0],
    [0,0,0,0,0,0,8,2,0,5,0],
    [0,2,9,0,0,6,7,0,0,0,0],
    [0,0,0,0,6,0,0,0,1,8,0],
    [0,0,0,7,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,6,0],
    [0,9,0,0,2,0,0,0,3,0,0],
    [0,1,0,0,7,0,0,0,0,0,0],
    [0,0,0,5,0,0,4,0,0,7,0],
    [0,0,0,0,0,0,0,0,0,0,0]
    ]
# test.set_num((7,2),3)
# test.set_num((8,3),4)
# test.add_arrow([(4,5),(5,6),(6,5)],[(5,4)])
# test.add_arrow([(8,9),(9,8),(8,7)],[(7,8)])
# test.add_pali([(3,1),(4,2),(4,3)])
# test.add_pali([(3,4),(3,5),(4,6)])
# test.add_pali([(6,4),(7,5),(7,6)])
# test.add_pali([(6,7),(6,8),(7,9)])
# test.add_little([(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9)],36)
# test.add_little([(1,6),(2,5),(3,4),(4,3),(5,2),(6,1)],33)
# test.add_little([(2,9),(1,8)],3)
# test.add_little([(4,9),(3,8),(2,7),(1,6)],15)
# test.add_little([(9,4),(8,5),(7,6),(6,7),(5,8),(4,9)],33)
# test.add_little([(8,1),(9,2)],3)
# test.print_constraints()
sudoku.print_board()
sudoku.sort_cells()
sudoku.solve()
sudoku.print_board()