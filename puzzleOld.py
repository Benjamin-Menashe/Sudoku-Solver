# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 08:55:36 2021

@author: Benjamin
"""

from valids import *

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
        
        self.cons_d = {(a,b):[] for a in range(1,10) for b in range(1,10)}
        
        self.func_dict = {
            'knight':valid_knight,
            'king':valid_king,
            'queen':valid_queen,
            'disjoint':valid_disjoint,
            'diag':valid_diag,
            'xsums':valid_xsums,
            'sandwich':valid_sandwich,
            'sky':valid_sky,
            'battle':valid_battle,
            'thermo':valid_thermo,
            'pali':valid_pali,
            'killer':valid_killer,
            'little':valid_little,
            'circle':valid_circle,
            'arrow':valid_arrow,
            'between':valid_between,
            'odd':valid_odd,
            'even':valid_even,
            'max':valid_max,
            'min':valid_min,
            'black':valid_black,
            'white':valid_white,
            'clone':valid_clone}
        
        self.full = False
        
        self.board_ind = []
        for i in range(1,10):
            for j in range(1,10):
                self.board_ind.append((i,j))
        
    def set_num(self, ind, num): # pick a position and place a number there
        self.board[ind[0]][ind[1]] = num
        
# %% adding constraints
    def add_knight(self, num = [0]):
        # num = list for which numbers the constraint applies LIST
            # 0 = 'all numbers'
        self.constraints.append('knight')
        for i in range(1,10):
            for j in range(1,10):
                self.cons[i][j].append(['knight',num])
                
    def add_king(self, num = [0]):
        # num = list for which numbers the constraint applies LIST
            # 0 = 'all numbers'
        self.constraints.append('king')
        for i in range(1,10):
            for j in range(1,10):
                self.cons[i][j].append(['king',num])

    def add_queen(self, num = [0]):
        # num = list for which numbers the constraint applies LIST
            # 0 = 'all numbers'
        self.constraints.append('queen')
        for i in range(1,10):
            for j in range(1,10):
                self.cons[i][j].append(['queen',num])
    
    def add_disjoint(self):
        # disjoint sets constraint
        self.constraints.append('disjoint')
        for i in range(1,10):
            for j in range(1,10):
                self.cons[i][j].append(['disjoint'])
                
    def add_xsums(self, ind, val):
        # ind must be on edge. sum of X numbers from that edge, where X is the val closest to edge, equals val.
        self.constraints.append('xsums')
        if ind[0] == 0: # down
            for i in range(1,10):
                self.cons[i][ind[1]].append(['xsums',(1,ind[1]),'d',val])
        elif ind[0] == 10: # up
            for i in range(1,10):
                self.cons[i][ind[1]].append(['xsums',(9,ind[1]),'u',val])
        elif ind[1] == 0: # right
            for i in range(1,10):
                self.cons[ind[0]][i].append(['xsums',(ind[0],1),'r',val])
        elif ind[1] == 10: # left
            for i in range(1,10):
                self.cons[ind[0]][i].append(['xsums',(ind[0],9),'l',val])
    
    def add_sandwich(self, ind, val, lower = 1, upper = 9):
            # ind must be on edge. sum of number from lower to upper must be val.
            # lower default 1, upper default 9
            self.constraints.append('sandwich')
            if ind[0] == 0: # vertical
                a = ind[1]
                self.cons[9][ind[1]].append(['sandwich',[(i,a) for i in range(1,10)],'v',val,lower,upper])
            elif ind[1] == 0: # horizontal
                a = ind[0]
                self.cons[ind[0]][9].append(['sandwich',[(a,i) for i in range(1,10)],'h',val,lower,upper])
            
    def add_sky(self, ind, val):
        # ind must be on edge. val is number of strictly increasing number from that edge
        self.constraints.append('sky')
        if ind[0] == 0: # down
            a = ind[1]
            self.cons[9][ind[1]].append(['sky',[(i,a) for i in range(1,10)],'d',val])
        elif ind[0] == 10: # up
            a = ind[1]
            self.cons[9][ind[1]].append(['sky',[(10-i,a) for i in range(1,10)],'u',val])
        elif ind[1] == 0: # right
            a = ind[0]
            self.cons[ind[0]][9].append(['sky',[(a,i) for i in range(1,10)],'r',val])
        elif ind[1] == 10: # left
            a = ind[0]
            self.cons[ind[0]][9].append(['sky',[(a,10-i) for i in range(1,10)],'l',val])
                
    def add_battle(self, ind, val):
        # ind must be on edge. val is sum of overalap / space when counting X cells from each edge of row/col.
        self.constraints.append('battle')
        if ind[0] == 0: # vertical
            a = ind[1]
            self.cons[9][ind[1]].append(['battle',[(i,a) for i in range(1,10)],'v',val])
        elif ind[1] == 0: # horizontal
            a = ind[0]
            self.cons[ind[0]][9].append(['battle',[(a,i) for i in range(1,10)],'h',val])

    def add_diag(self, kind='both'):
        # kind = 'up' / 'down' / 'both' STR
        self.constraints.append('diag')
        if kind == 'up':
            spots = [(9,1),(8,2),(7,3),(6,4),(5,5),(4,6),(3,7),(2,8),(1,9)]
            for k in range(9):
                self.cons[spots[k][0]][spots[k][1]].append(['diag',spots,k])
        elif kind == 'down':
            spots = [(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9)]
            for k in range(9):
                self.cons[spots[k][0]][spots[k][1]].append(['diag',spots,k])
        else:
            self.add_diag(kind='up')
            self.add_diag(kind='down')
                
    def add_thermo(self, ind_list):
        # ind_list = list of indices for thermo, order: smallest to largest LIST(TUP)
        self.constraints.append('thermo')
        for k in range(len(ind_list)):
            self.cons[ind_list[k][0]][ind_list[k][1]].append(['thermo',ind_list,k])

    def add_pali(self, ind_list):
        # ind_list = list of indices for palindrom, order matters LIST(TUP)
        self.constraints.append('pali')
        for k in range(len(ind_list)):
            self.cons[ind_list[k][0]][ind_list[k][1]].append(['pali',ind_list,k])
            
    def add_killer(self, ind_list, val):
        # ind_list = list of relevent indices. Digits may repeat
        # val = sum of the relevent digits
        self.constraints.append('killer')
        for k in range(len(ind_list)):
            self.cons[ind_list[k][0]][ind_list[k][1]].append(['killer',ind_list,val])
            
    def add_little(self, ind_list, val):
        # ind_list = list of relevent indices. Digits may repeat
        # val = sum of the relevent digits
        self.constraints.append('little')
        for k in range(len(ind_list)):
            self.cons[ind_list[k][0]][ind_list[k][1]].append(['little',ind_list,val])
    
    def add_circle(self, ind_list, num_list):
        # ind_list = list of relevent indices
        # num_list = list of numbers that must go in the ind_list
        self.constraints.append('circle')
        for k in range(len(ind_list)):
            self.cons[ind_list[k][0]][ind_list[k][1]].append(['circle',ind_list,num_list])
    
    def add_arrow(self, ind_list, ind_val):
        # ind_list = list of ind for cluster body LIST(TUP)
        # ind_val = ind for the value, 1 IND or 2 IND, order matters LIST(TUP)
        self.constraints.append('arrow')
        for k in range(len(ind_list)):
            self.cons[ind_list[k][0]][ind_list[k][1]].append(['arrow',ind_list,ind_val])
        for k in range(len(ind_val)):
            self.cons[ind_val[k][0]][ind_val[k][1]].append(['arrow',ind_list,ind_val])
    
    def add_between(self, ind_list, ind_edge):     
        # ind_list = list of ind for cluster body LIST(TUP)
        # ind_edge = 2 ind for the edges LIST(TUP)
        self.constraints.append('between')
        for k in range(len(ind_list)):
            self.cons[ind_list[k][0]][ind_list[k][1]].append(['between',ind_list,ind_edge])
        for k in range(len(ind_edge)):
            self.cons[ind_edge[k][0]][ind_edge[k][1]].append(['between',ind_list,ind_edge])
        
    def add_odd(self, ind):
        # ind = index of cell TUP
        self.constraints.append('parity')
        self.cons[ind[0][ind[1]]].append(['odd'])
        
    def add_even(self, ind):
        # ind = index of cell TUP
        self.constraints.append('parity')
        self.cons[ind[0][ind[1]]].append(['even'])

    def add_min(self, ind):
        # ind = index of cell TUP
        self.constraints.append('local')
        spots = [(ind[0]-1,ind[1]),(ind[0]+1,ind[1]),(ind[0],ind[1]-1),(ind[0],ind[1]+1)]
        spots = list(filter(lambda t: 0 < t[0] < 10 and 0 < t[1] < 10, spots))
        for k in range(len(spots)):
            self.cons[spots[k][0]][spots[k][1]].append(['max',[ind]])
        self.cons[ind[0]][ind[1]].append(['min',spots])

    def add_max(self, ind):
        # ind = index of cell TUP
        self.constraints.append('local')
        spots = [(ind[0]-1,ind[1]),(ind[0]+1,ind[1]),(ind[0],ind[1]-1),(ind[0],ind[1]+1)]
        spots = list(filter(lambda t: 0 < t[0] < 10 and 0 < t[1] < 10, spots))
        for k in range(len(spots)):
            self.cons[spots[k][0]][spots[k][1]].append(['min',[ind]])
        self.cons[ind[0]][ind[1]].append(['max',spots])
        
    def add_krokpi_black(self, ind_list, ratio=1/2):
        # ind_list = 2 cells that are in ratio relation LIST(TUP)
        # ratio = expressed as fraction. default 1:2
        self.constraints.append('kropki')
        for k in range(2):
            self.cons[ind_list[k][0]][ind_list[k][1]].append(['black', ind_list, (k+1)%2, ratio])
            
    def add_krokpi_white(self, ind_list, diff=1):
        # ind_list = 2 cells that are in diff relation LIST(TUP)
        # diff = difference. default 1 (consecutive)
        self.constraints.append('kropki')
        for k in range(2):
            self.cons[ind_list[k][0]][ind_list[k][1]].append(['white', ind_list, (k+1)%2, diff])
        
    def add_clone(self, ind_list):
        # ind_list = list of 2 TUP where number must equal LIST(TUP)
        self.constraints.append('clone')
        a = ind_list[0]
        b = ind_list[1]
        self.cons[a[0]][a[1]].append(['clone',b])
        self.cons[b[0]][b[1]].append(['clone',a])
        
# %% a func to loop through all constraints of the cell and check constraints

    def valid(self, ind, num):       
        
        if not valid_normal(self.board, ind, num): # always check normal
            return False
        
        cell_cons = self.cons[ind[0]][ind[1]]
        for c in range(len(cell_cons)):
            if not self.func_dict[cell_cons[c][0]](self.board, ind, cell_cons[c], num):
                return False
        
        return True
            
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
            if self.valid(ind, v):
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
                        
