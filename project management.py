# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 10:23:27 2021

@author: Benjamin
"""

# SUDOKU SOLVER
# for now just normal rules. Want to add:
    # whole board constraints:
        # knight                                {VV}
        # king                                  {VV}
        # queen                                 {VV}
        # disjoint sets                         {VV}
    
    # edge (whole row/col) constraints:
        # X-sums                                {VV}
        # sandwich                              {VV}
        # skyscraper                            {VV}
        # battlefield                           {VV}        
    
    # 1 cluster of cells constraints (no val):
        # diagonals (seperated in function)     {VV}
        # thermos (include >)                   {VV}
        # palindromes                           {VV}
        
    # 2 cluster of cells constraints (set val)
        # killer                                {VV}
        # (magic square is just complex killer)
        # (XV is basically killer 10 5)
        # little killer                         {VV}
        # circles                               {VV}
        
    # 3 cluster of cells constraints (val within cells)
        # arrow (include double arrow)          {VV}
        # between lines                         {VV}
    
    # kropki
        # black (1:2 or any ratio)              {VV}
        # white (consecutive or any diff)       {VV}
        # (don't forget negative constraint)    {}
    
    # One cell constraints:
        # odds                                  {VV}
        # evens                                 {VV}
        # local min                             {VV}
        # local max                             {VV}
        
        # clone                                 {VV}
        

# add checks and balances
# add shortcuts
    
# need to add:
    # kropki negative constraint
    # negative XV constraint
    # killer with unknown sum
    # irregular
    
# need to add torus board for certain constraints
    
# also want to add GUI for input the sudoku problem instead of typing