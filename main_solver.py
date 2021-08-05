# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 20:11:54 2021

@author: Benjamin
"""

from puzzle import puzzle
from valids import *
import time


sudoku = puzzle()

# %% set numbers using 'sudoku.set_sum'

# %% add constraints using various 'sudoku.add_XXX' functions

## KILLER EXAMPLE
# sudoku.add_killer([(1,1),(2,1)],14)
# sudoku.add_killer([(3,1),(4,1)],14)
# sudoku.add_killer([(1,2),(1,3),(1,4),(1,5)],28)
# sudoku.add_killer([(3,3),(4,3),(5,3),(6,3),(7,3)],33)
# sudoku.add_killer([(3,5),(4,5),(5,5),(6,5),(7,5)],17)
# sudoku.add_killer([(3,7),(4,6),(4,7)],23)
# sudoku.add_killer([(6,6),(6,7)],6)
# sudoku.add_killer([(6,8),(6,9)],6)
# sudoku.add_killer([(7,4),(8,4)],15)
# sudoku.add_killer([(9,4),(9,5),(9,6)],8)
# sudoku.add_killer([(8,7),(9,7)],6)
# sudoku.add_killer([(9,8),(9,9)],15)
# sudoku.add_killer([(2,9),(3,9),(4,9),(5,9)],12)

## ARROW-KILLER-LITTLE EXAMPLE
# sudoku.set_num((7,2),3)
# sudoku.set_num((8,3),4)
# sudoku.add_little([(8,1),(9,2)],3)
# sudoku.add_little([(2,9),(1,8)],3)
# sudoku.add_arrow([(3,7),(4,7)],[(2,8)])
# sudoku.add_arrow([(2,1),(1,2),(2,3)],[(3,2)])
# sudoku.add_arrow([(4,5),(5,6),(6,5)],[(5,4)])
# sudoku.add_arrow([(8,9),(9,8),(8,7)],[(7,8)])
# sudoku.add_little([(4,9),(3,8),(2,7),(1,6)],15)
# sudoku.add_little([(1,6),(2,5),(3,4),(4,3),(5,2),(6,1)],33)
# sudoku.add_little([(9,4),(8,5),(7,6),(6,7),(5,8),(4,9)],33)
# sudoku.add_little([(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9)],36)
# sudoku.add_pali([(3,1),(4,2),(4,3)])
# sudoku.add_pali([(3,4),(3,5),(4,6)])
# sudoku.add_pali([(6,4),(7,5),(7,6)])
# sudoku.add_pali([(6,7),(6,8),(7,9)])

# ARROW-KILLER EXAMPLE
# sudoku.set_num((8,1),6)
# sudoku.add_killer([(3,2),(3,3),(4,3),(5,3),(6,3)],29)
# sudoku.add_arrow([(2,3),(3,2),(4,3)],[(1,4)])
# sudoku.add_killer([(4,6),(5,4),(5,5),(5,6),(6,4)],25)
# sudoku.add_arrow([(5,4),(6,4)],[(7,3)])
# sudoku.add_arrow([(4,6),(5,6)],[(3,7)])
# sudoku.add_killer([(4,8),(5,8),(6,7),(6,8),(7,8)],30)
# sudoku.add_arrow([(8,7),(7,8),(6,8)],[(9,6)])
# sudoku.add_killer([(7,1),(8,1),(7,2),(7,3)],18)
# sudoku.add_arrow([(8,1),(7,1),(6,2)],[(9,2)])
# sudoku.add_killer([(2,9),(3,7),(3,8),(3,9)],19)
# sudoku.add_arrow([(2,8),(3,8),(4,9)],[(1,9)])
# sudoku.add_killer([(7,5),(8,5),(9,5),(9,6)],15)
# sudoku.add_killer([(1,4),(1,5),(2,5),(3,5)],20)
# sudoku.add_killer([(2,6),(3,6)],10)

# %% use 'sudoku.sort_cells' to sort the cells by constraints
sudoku.sort_cells()

# %% solve the board using 'sudoku.solve'
start = time.time()
sudoku.solve()
end = time.time()
print(end - start)

# %% print solution using 'sudoku.print_board'
sudoku.print_board()
