# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 08:55:36 2021

@author: Benjamin
"""
# %% define board and dictionaries
class puzzle:
    def __init__(self):
        self.board = [
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0]
    ]
        
        self.constraints = [] # list of all constraint names for the solve function
        
        # for each constraint, write inside self.con_details with the details
        self.cons = [[[],[],[],[],[],[],[],[],[],[]],
                     [[],[],[],[],[],[],[],[],[],[]],
                     [[],[],[],[],[],[],[],[],[],[]],
                     [[],[],[],[],[],[],[],[],[],[]],
                     [[],[],[],[],[],[],[],[],[],[]],
                     [[],[],[],[],[],[],[],[],[],[]],
                     [[],[],[],[],[],[],[],[],[],[]],
                     [[],[],[],[],[],[],[],[],[],[]],
                     [[],[],[],[],[],[],[],[],[],[]],
                     [[],[],[],[],[],[],[],[],[],[]]]
        
        self.full = False
        
        self.board_ind = []
        for i in range(1,10):
            for j in range(1,10):
                self.board_ind.append((i,j))
        
    def set_num(self, ind, num): # pick a position and place a number there
        self.board[ind[0]][ind[1]] = num
        
# %% adding constraints
    def add_knight(self,num = [0]):
        # num = list for which numbers the constraint applies LIST
            # 0 = 'all numbers'
        self.constraints.append('knight')
        for i in range(1,10):
            for j in range(1,10):
                self.cons[i][j].append(['knight',num])
                
    def add_king(self,num = [0]):
        # num = list for which numbers the constraint applies LIST
            # 0 = 'all numbers'
        self.constraints.append('king')
        for i in range(1,10):
            for j in range(1,10):
                self.cons[i][j].append(['king',num])

    def add_queen(self,num = [0]):
        # num = list for which numbers the constraint applies LIST
            # 0 = 'all numbers'
        self.constraints.append('queen')
        for i in range(1,10):
            for j in range(1,10):
                self.cons[i][j].append(['queen',num])
                
    def add_thermo(self,ind_list):
        # ind_list = list of indices for thermo, order: smallest to largest LIST(TUP)
        self.constraints.append('thermo')
        for k in range(len(ind_list)):
            self.cons[ind_list[k][0]][ind_list[k][1]].append(['thermo',ind_list,k])
            
        
# %% checking valids for each constraint

    def valid_normal(puz, ind, num): 
        # checks if num (INT) is valid in ind (TUP) by normal rules  
            # check row
        for j in range(1,10):
            if puz.board[ind[0]][j] == num and ind[1] != j:
                return False            
        # check col
        for i in range(1,10):
            if puz.board[i][ind[1]] == num and ind[0] != i:
                return False                
        # check square
        box_x = (ind[1]-1) // 3
        box_y = (ind[0]-1) // 3
        for i in range(box_y*3 + 1, box_y*3 + 4):
            for j in range(box_x*3 + 1, box_x*3 + 4):
                if puz.board[i][j] == num and (i,j) != ind:
                    return False                
        return True

    def valid_knight(puz, ind, inf, num):
        # inf = ['knight',[nums]]
        # make list, filter it, and check it
        if num in inf[1] or inf[1]==0:
            i = ind[0]
            j = ind[1]
            spots = [(i-2,j-1),(i-2,j+1),(i+2,j-1),(i+2,j+1),(i-1,j-2),(i-1,j+2),(i+1,j-2),(i+1,j+2)]
            spots = list(filter(lambda t: 0 < t[0] < 10 and 0 < t[1] < 10, spots))
            for k in range(len(spots)):
                if puz.board[spots[k][0]][spots[k][1]] == num:
                    return False
            return True
        return True
    
    def valid_thermo(puz, ind, inf, num):
        # inf = ['thermo',ind_list,k]
        if inf[2] > 0:
            for k in range(inf[2]):
                if num <= puz.board[inf[1][k][0]][inf[1][k][1]]:
                    return False
            return True
        return True

# %% a func to loop through all constraints of the cell and check constraints

    def valid(puz, ind, num):
        if not valid_normal(puz, ind, num): # always check normal
            return False
        
        cell_cons = puz.cons[ind[0]][ind[1]]
        for c in range(len(cell_cons)):
            cur_con = cell_cons[c][0]
            
            

# %% solver - a func to recursively check each cell and each number

    def find_empty(self):
        # finds a 0 in the board
        # if found, returns that ind TUP
        # if not, returns NONE
        for i in range(1,10):
            for j in range(1,10):
                if self.board[i][j] == 0:
                    return (i,j)
        return None
    
    def solve(self):
        ind = self.find_empty()
        if not ind:
            return True
        
        for v in range(1,10):
            if self.valid(self, ind, v):
                self.board[ind[0]][ind[1]] = v
                
                if self.solve(): # recursion
                    return True
                
                self.board[ind[0]][ind[1]] = 0 # reset
        
        return False # no solution
        

# %% printer

    def print_constraints(self):
        print('The current constraints in this board are:')
        print(set(self.constraints))
    
    def print_board(self, full = None):
        # full = with / without edges BOOL
        if full == None:
            full = self.full
        if full == True:
            for i in range(11): # over rows
                if i % 3 == 1:
                    print('   -------------------------------   ')        
                for j in range(11): # over cols
                    if j % 3 == 1:
                        if i in [0,10]:
                            print(' ', end="")
                        else:
                            print('|', end="")            
                    if  j == 10: # end of row
                        print(self.board[i][j])
                    else:
                        if self.board[i][j] < 10:
                            print(str(self.board[i][j]) + "  ", end = "")
                        else:
                            print(str(self.board[i][j]) + " ", end = "")
        else: 
            for i in range(1,10): # over rows
                if i % 3 == 1 and i != 1:
                    print('---------------------')        
                for j in range(1,10): # over cols
                    if j % 3 == 1 and j !=1:
                        print('| ', end="")            
                    if  j == 9: # end of row
                        print(self.board[i][j])
                    else:
                        print(str(self.board[i][j]) + " ", end = "")
                        
# %% for testing code

test = puzzle()
test.add_knight()
test.add_king([1,3,5,7,9])

test.add_thermo([(1,1),(1,2),(1,3),(2,4)])

test.print_constraints()
