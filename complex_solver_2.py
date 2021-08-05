# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 10:24:36 2021

@author: Benjamin
"""

# Indices rules: (row,col) TUP
    # board is between (1,1) - (9,9)
    # upper edge (0,0)-(0,10)
    # lower edge (10,0)-(10,10)
    # left edge (0,0)-(10,0)
    # right edge (0,10)-(10,10)

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
        self.con_details = {
            'knight':[False],
            'king':[False],
            'queen':[False]}
        
        self.full = False
        
        self.board_ind = []
        for i in range(1,10):
            for j in range(1,10):
                self.board_ind.append((i,j))
        
        self.con_regions = []
        
    def set_num(self, ind, num): # pick a position and place a number there
        self.board[ind[0]][ind[1]] = num
        
# %% Adding Constraints
        
    def add_diag(self,kind='both'):
        # kind = 'up' / 'down' / 'both' STR
        self.constraints.append('diag')
        self.con_regions.append([('diag', kind)])

        
    def add_whole(self,kind,num=[0]):
        # kind = 'knight' / 'king' / 'queen' STR
        # num = list for which numbers the constraint applies LIST
            # 0 = 'all numbers'
        self.constraints.append(kind)
        self.con_details[kind] = [True,num]
    
    def add_edge(self, kind, ind, val):
        # kind = 'xsums' / 'sandwich' / 'skyscraper' / 'battlefield' STR
        # ind = ind of edge for which the constraint applies TUP
        # val = value of constraint INT
        self.constraints.append(kind)
        self.board[ind[0]][ind[1]] = val
        if self.con_details[kind] == False:
            self.con_details[kind] = [True]
        self.con_details[kind].append([ind,val])
        self.full = True
        
    def add_cluster1(self, kind, ind_list):
        # kind = 'thermo' / 'pali' / 'dup' STR
        # ind_list = list of indices for cluster LIST(TUP)
            # IMPORTANT - order matters!
                # thermo - smallest to largest
                # pali - by palindrome order
        self.constraints.append(kind)
        self.con_regions.append((kind, ind_list))
        
    def add_cluster2(self, kind, ind_list, val):
        # kind = 'killer' / 'little' / 'circle' STR
        # ind_list = list of indices for cluster LIST(TUP)
        # val = can be 3 things:
            # sum for killer / little INT
            # unknown sum for killer / little STR ('A','B',...)
            # list for circle LIST
        self.constraints.append(kind)
        self.con_regions.append([(kind, ind_list, val)])
    
    def add_cluster3(self,kind,ind_list,ind_val):
        # kind = 'arrow' / 'between' STR
        # ind_list = list of ind for cluster body LIST(TUP)
        # ind_val = ind for the value TUP/LIST
            # for 'arrow' = 1 IND or 2 IND, order matters
            # for 'between' = 2 IND
        self.constraints.append(kind)
        self.con_regions.append([(kind, ind_list, ind_val)])
        
    def add_kropki(self,kind,ind_list=None,negative=False,ratio=(1,2),diff=1):
        # kind = 'black' / 'white' STR
        # ind_list = list of 2 ind for kropki LIST(TUP)
            # if ind_list = None, only negative constraints apply (makes negative=True)
        # negative = negative constraints apply BOOL
        # ratio = for black dots, ratio of cells TUP
        # diff = for white dots, difference between them INT
        self.constraints.append(kind)
        if ind_list == None: # automatic negative constraint flipper
            negative = True
        if kind == 'black':
            self.con_regions.append([(kind, ind_list, ratio)])
        elif kind == 'white':
            self.con_regions.append([(kind, ind_list, diff)])
        
    def add_cell(self, kind, ind):
        # kind = 'odd' / 'even' / 'min' / 'max' STR
        # ind = index of cell TUP
        self.constraints.append(kind)
        self.con_regions.append([(kind, ind)])
        
    def rm_con(self, kind='all'): # delete ALL OCCURANCES of constraint kind
        if kind != 'all':
            self.constraints = [x for x in self.constraints if x != kind]
            if kind in ['king', 'knight', 'queen']:    
                self.con_details[kind] = False
            else:
                self.con_regions = [x for x in self.con_regions if x[0] != kind]
        else:
            self.constraints = []
            self.con_regions = []
        

# %% Valid checkers
    
    def valid_normal(self, ind, num): 
        # checks if num (INT) is valid in ind (TUP) by normal rules        
            # check row
        for j in range(1,10):
            if self.board[ind[0]][j] == num and ind[1] != j:
                return False            
        # check col
        for i in range(1,10):
            if self.board[i][ind[1]] == num and ind[0] != i:
                return False                
        # check square
        box_x = (ind[1]-1) // 3
        box_y = (ind[0]-1) // 3
        for i in range(box_y*3 + 1, box_y*3 + 4):
            for j in range(box_x*3 + 1, box_x*3 + 4):
                if self.board[i][j] == num and (i,j) != ind:
                    return False                
        return True
    
    def valid_diag(self, ind, num, region='both'):
        if region == 'up':
            spots = [(9,1),(8,2),(7,3),(6,4),(5,5),(4,6),(3,7),(2,8),(1,9)]
        elif region == 'down':
            spots = [(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9)]
        else:
            up = self.valid_diag(ind,num,region='up')
            down = self.valid_diag(ind,num,region='down')
            return (up and down)
        for k in range(len(spots)):
            if self.board[spots[k][0]][spots[k][1]] == num and spots[k] != ind:
                return False
        return True 
        
    def valid_knight(self, ind, num):
        # checks knight constraint
        # make list, filter it, and check it
        i = ind[0]
        j = ind[1]
        spots = [(i-2,j-1),(i-2,j+1),(i+2,j-1),(i+2,j+1),(i-1,j-2),(i-1,j+2),(i+1,j-2),(i+1,j+2)]
        spots = list(filter(lambda t: 0 < t[0] < 10 and 0 < t[1] < 10, spots))
        for k in range(len(spots)):
            if self.board[spots[k][0]][spots[k][1]] == num:
                return False
        return True
    
    def valid_king(self, ind, num):
        # checks king constraint 
        # make list, filter it, and check it
        i = ind[0]
        j = ind[1]
        spots = [(i-1,j-1),(i-1,j+1),(i+1,j-1),(i+1,j+1)]
        spots = list(filter(lambda t: 0 < t[0] < 10 and 0 < t[1] < 10, spots))
        for k in range(len(spots)):
            if self.board[spots[k][0]][spots[k][1]] == num:
                return False
        return True
    
    def valid_queen(self, ind, num):
        # checks queen constraint    
        # make list, filter it, and check it
        i = ind[0]
        j = ind[1]
        s1 = [(i+a,j+a) for a in range(-8,9)]
        s2 = [(i+a,j-a) for a in range(-8,9)]
        spots = s1+s2
        spots = list(filter(lambda t: 0 < t[0] < 10 and 0 < t[1] < 10, spots))
        for k in range(len(spots)):
            if self.board[spots[k][0]][spots[k][1]] == num and spots[k] != ind:
                return False
        return True
    
    def valid_thermo(self, ind_list, k, num):
        # checks thermo constraint on whole region ind_list (LIST(TUP))
        if k == 0:
            return True
        elif num < self.board[ind_list[k-1][0]][ind_list[k-1][1]]:
                return False
        return True
    
    def valid_pali(self, ind_list, k, num):
        # checks pali constraint on whole region ind_list (LIST(TUP))
        if k < len(ind_list+1)//2:
            return True
        elif num != self.board[ind_list[-(k+1)][0]][ind_list[-(k+1)][1]]:
                return False
        return True
    
    def valid_killer(self, ind_list, val):
        # checks killer constraint on whole region ind_list (LIST(TUP))
        nums = [self.board[ind_list[t][0]][ind_list[t][1]] for t in range(len(ind_list))]
        if len(nums) != len(set(nums)):
            return False
        if sum(nums) != val:
            return False
        return True
    
    def valid_little(self, ind_list, val):
        # checks little killer constraint on whole region ind_list (LIST(TUP))
        sam = sum([self.board[ind_list[t][0]][ind_list[t][1]] for t in range(len(ind_list))])
        if sam == val:
            return True
        return False
    
    def valid_circles(self, ind_list, val_list):
        # checks if vals in ind_list (LIST(TUP) contain all vals in val_list (LIST))
        nums = [self.board[ind_list[t][0]][ind_list[t][1]] for t in range(len(ind_list))]
        for k in range(len(val_list)):
            if val_list[k] not in nums:
                return False
        return True
    
    def valid_arrow(self,ind_list, ind_val):
        # checks is sum of vals in in_list equals value in ind_val
        vals = [self.board[ind_val[t][0]][ind_val[t][1]] for t in range(len(ind_val))]
        val = int("".join(([str(vals[k]) for k in range(len(vals))])))
        sam = sum([self.board[ind_list[t][0]][ind_list[t][1]] for t in range(len(ind_list))])
        if sam != val:
            return False
        return True
    
    def valid_between(self, ind_list, ind_val):
        # checks between constraint by making sure none in ind_list is bigger than max(ind_val) or smaller than min(ind_val)
        nums = [self.board[ind_list[t][0]][ind_list[t][1]] for t in range(len(ind_list))]
        vals = [self.board[ind_val[t][0]][ind_val[t][1]] for t in range(len(ind_val))]
        maxwell = max(vals)
        minerva = min(vals)
        for k in range(len(nums)):
            if nums[k] >= maxwell or nums[k] <= minerva:
                return False
        return True
    
    def valid_black_pos(self, ind_list, ratio):
        # checks if 2 nums in ind_list LIST(TUP) are in ratio TUP
        targ_rat = ratio[0]/ratio[1]
        a1 = ind_list[0][0]
        a2 = ind_list[0][1]
        b1 = ind_list[1][0]
        b2 = ind_list[1][1]
        act_rat = self.board[a1][a2] / self.board[b1][b2]
        if act_rat != targ_rat and act_rat != 1 / targ_rat:
            return False
        return True
    
    def valid_white_pos(self, ind_list, diff):
        # checks if 2 nums in ind_list LIST(TUP) are in distance diff INT
        a1 = ind_list[0][0]
        a2 = ind_list[0][1]
        b1 = ind_list[1][0]
        b2 = ind_list[1][1]
        act_diff = self.board[a1][a2] - self.board[b1][b2]
        if act_diff != diff and act_diff != -diff:
            return False
        return True       
    
    def valid_black_neg(self, ind_list, ratio):
        # checks if 2 nums in ind_list LIST(TUP) are not in ratio TUP
        targ_rat = ratio[0]/ratio[1]
        a1 = ind_list[0][0]
        a2 = ind_list[0][1]
        b1 = ind_list[1][0]
        b2 = ind_list[1][1]
        act_rat = self.board[a1][a2] / self.board[b1][b2]
        if act_rat == targ_rat or act_rat == 1 / targ_rat:
            return False
        return True
    
    def valid_white_neg(self, ind_list, diff):
        # checks if 2 nums in ind_list LIST(TUP) are not in distance diff INT
        a1 = ind_list[0][0]
        a2 = ind_list[0][1]
        b1 = ind_list[1][0]
        b2 = ind_list[1][1]
        act_diff = self.board[a1][a2] - self.board[b1][b2]
        if act_diff == diff or act_diff == -diff:
            return False
        return True

# %% meta valids

    def valid_whole(self, ind, num):
        king = self.con_details['king'][0]
        knight = self.con_details['knight'][0]
        queen = self.con_details['queen'][0]
        
        a = True
        b = True
        c = True
            
        if king and (num in self.con_details['king'][1] or 0 in self.con_details['king'][1]):
            a = self.valid_king(ind,num)
        if knight and (num in self.con_details['knight'][1] or 0 in self.con_details['knight'][1]):
            b = self.valid_knight(ind,num)
        if queen and (num in self.con_details['queen'][1]):
            c = self.valid_queen(ind,num)
        
        if self.valid_normal(ind, num) and a and b and c:
            return True
        return False
    
    def valid_region(self, kind, region, ind, num):
        if kind == 'diag':
            a = self.valid_diag(ind, num, region)
        elif kind == 'thermo':
            k = region.index(ind)
            a = self.valid_thermo(region, k, num)
        
        b = self.valid_whole(ind, num)
        
        if a and b:
            return True
        return False
    
# %% Solver
    
    def find_empty(self, region):
        # finds a 0 within a line / cluster / whole board LIST(TUP)
        # if found, returns that ind TUP
        # if not, returns NONE (region solved)
        for t in range(len(region)):
            if self.board[region[t][0]][region[t][1]] == 0:
                return region[t]
        return None
        
    def solve_normal(self, region = 0):
        if region == 0:
            region = self.board_ind
        find = self.find_empty(region)
        if not find:
            return True
        
        for i in range(1,10):
            if self.valid_whole(find, i):
                self.board[find[0]][find[1]] = i
                
                if self.solve_normal(region):
                    return True
                self.board[find[0]][find[1]] = 0 # reset
        
        return False
     
    def solve(self, i = 0): # at the end make cons_dict = self.con_details
    
        lenny = len(self.con_regions)
        
        if lenny == i:
            a = self.solve_normal()  
            return a
        else:
            kind = self.con_regions[i][0]
            region = self.con_regions[i][1]
    
    
            find = self.find_empty(region)
            if not find:
                i += 1            
                return self.solve(i)
            
            for j in range(1,10):
                if self.valid_region(kind, region, find, j):
                    self.board[find[0]][find[1]] = j
                
                    if self.solve(i): # if it is solved (i.e.) not empty, move to next constraint
                        i += 1
                        return self.solve(i)
                    
                    self.board[find[0]][find[1]] = 0
            
            return False
            
# %% Print
        
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
        
# %% For Testing...
test = puzzle()
# test.set_num((1,1), 7)
# test.set_num((1,4), 2)
# test.set_num((2,7), 6)
# test.set_num((4,2), 3)
# test.set_num((4,8), 8)
# test.set_num((6,1), 9)
# test.set_num((6,2), 5)
# test.set_num((6,8), 4)
# test.set_num((6,9), 3)
# test.set_num((7,1), 3)
# test.set_num((7,8), 9)
# test.set_num((7,9), 8)
# test.set_num((8,3), 1)
# test.set_num((8,7), 2)
# test.set_num((9,1), 5)
# test.set_num((9,4), 7)
# test.set_num((9,6), 8)
# test.set_num((9,9), 4)
# test.add_whole('knight')

test.add_cluster1('thermo', [(1,7),(2,6),(3,5),(2,2),(1,3),(1,2)])
test.add_cluster1('thermo', [(7,1),(6,1),(5,1),(4,1),(3,2),(3,3)])
test.add_cluster1('thermo', [(6,3),(5,3)])
test.add_cluster1('thermo', [(6,7),(5,6),(5,5),(5,4)])
test.add_cluster1('thermo', [(5,9),(6,9),(7,8),(8,7)])
test.add_cluster1('thermo', [(9,3),(8,4),(7,5),(8,6),(9,7),(9,8)])

test.print_board()
test.solve()

test.print_board()
