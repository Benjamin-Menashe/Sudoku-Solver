# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 20:09:12 2021

@author: Benjamin
"""
# %% functions to find numbers and indices

def has_num(bo, reg, num=0):
    # reg = ind_list
    # returns TRUE if the num is in the board region, FALSE otherwise    
    for t in range(len(reg)):
        if bo[reg[t][0]][reg[t][1]] == num:
            return True
    return False

def find_num(bo, reg, num):
    # reg = ind_list
    # returns pos of the ind of number (out of region), FALSE if no such number exists
    for t in range(len(reg)):
        if bo[reg[t][0]][reg[t][1]] == num:
            return t
    return False

# %% valid checking functions

def valid_normal(bo, ind, num): 
    # checks if num (INT) is valid in ind (TUP) by normal rules  
    for j in range(1,10): # check row
        if bo[ind[0]][j] == num and ind[1] != j:
            return False            
    for i in range(1,10): # check col
        if bo[i][ind[1]] == num and ind[0] != i:
            return False                
    # check square
    box_x = (ind[1]-1) // 3
    box_y = (ind[0]-1) // 3
    for i in range(box_y*3 + 1, box_y*3 + 4):
        for j in range(box_x*3 + 1, box_x*3 + 4):
            if bo[i][j] == num and (i,j) != ind:
                return False                
    return True

def valid_knight(bo, ind, inf, num):
    # inf = ['knight', [nums]]
    # make list, filter it, and check it
    if num in inf[1] or 0 in inf[1]:
        i = ind[0]
        j = ind[1]
        spots = [(i-2,j-1),(i-2,j+1),(i+2,j-1),(i+2,j+1),(i-1,j-2),(i-1,j+2),(i+1,j-2),(i+1,j+2)]
        spots = list(filter(lambda t: 0 < t[0] < 10 and 0 < t[1] < 10, spots))
        for k in range(len(spots)):
            if bo[spots[k][0]][spots[k][1]] == num:
                return False
    return True
    
def valid_king(bo, ind, inf, num):
    # inf = ['king', [nums]]
    if num in inf[1] or 0 in inf[1]:
        i = ind[0]
        j = ind[1]
        spots = [(i-1,j-1),(i-1,j+1),(i+1,j-1),(i+1,j+1)]
        spots = list(filter(lambda t: 0 < t[0] < 10 and 0 < t[1] < 10, spots))
        for k in range(len(spots)):
            if bo[spots[k][0]][spots[k][1]] == num:
                return False
    return True

def valid_queen(bo, ind, inf, num):
    # inf = ['queen', [nums]]
    if num in inf[1] or 0 in inf[1]:
        i = ind[0]
        j = ind[1]
        spots = [(i+a,j+a) for a in range(-8,9)] + [(i+a,j-a) for a in range(-8,9)]
        spots = list(filter(lambda t: 0 < t[0] < 10 and 0 < t[1] < 10, spots))
        for k in range(len(spots)):
            if bo[spots[k][0]][spots[k][1]] == num and spots[k] != ind:
                return False
    return True

def valid_disjoint(bo, ind, inf, num):
    # inf = ['disjoint']
    i = ind[0]
    j = ind[1]
    spots = [(i+a,j+b) for a in range(-6,7,3) for b in range(-6,7,3)]
    spots = list(filter(lambda t: 0 < t[0] < 10 and 0 < t[1] < 10, spots))
    for k in range(len(spots)):
        if bo[spots[k][0]][spots[k][1]] == num and spots[k] != ind:
            return False
    return True

def valid_xsums(bo, ind, inf, num):
    # inf = ['xsums',X_ind,direction,val]
    bo[ind[0]][ind[1]] = num
    if bo[inf[1][0]][inf[1][1]] != 0:
        x = bo[inf[1][0]][inf[1][1]]
        sam = 0
        for i in range(1,x+1):
            if inf[2] == 'd':
                if bo[i][ind[1]] == 0:
                    bo[ind[0]][ind[1]] = 0
                    return True
                sam += bo[i][ind[1]]
            elif inf[2] == 'u':
                if bo[-(i+1)][ind[1]] == 0:
                    bo[ind[0]][ind[1]] = 0
                    return True
                sam += bo[-(i+1)][ind[1]]
            elif inf[2] == 'r':
                if bo[ind[0]][i] == 0:
                    bo[ind[0]][ind[1]] = 0
                    return True
                sam += bo[ind[0]][i]
            elif inf[2] == 'l':
                if bo[ind[0]][-(i+1)] == 0:
                    bo[ind[0]][ind[1]] = 0
                    return True
                sam += bo[ind[0]][-(i+1)]
        if sam != inf[3]:
            bo[ind[0]][ind[1]] = 0
            return False
    bo[ind[0]][ind[1]] = 0
    return True

def valid_sandwich(bo, ind, inf, num):
    # inf = ['sandwich', ind_list, dir, val, lower, upper]
    bo[ind[0]][ind[1]] = num
    a = find_num(bo, inf[1], inf[4])
    b = find_num(bo, inf[1], inf[5])
    sam = 0
    for k in range((min(a,b))+1,max(a,b)):
        sam += bo[inf[1][k][0]][inf[1][k][1]]
    if sam != inf[3]:
        bo[ind[0]][ind[1]] = 0
        return False
    bo[ind[0]][ind[1]] = 0
    return True

def valid_sky(bo, ind, inf, num):
    # inf = ['sky', ind_list, dir, val,]
    bo[ind[0]][ind[1]] = num
    blds = 1
    maxwell = bo[inf[1][0][0]][inf[1][0][1]]
    for k in range(1,9):
        if bo[inf[1][k][0]][inf[1][k][1]] > maxwell:
            maxwell = bo[inf[1][k][0]][inf[1][k][1]]
            blds += 1
    if blds != inf[3]:
        bo[ind[0]][ind[1]] = 0
        return False
    bo[ind[0]][ind[1]] = 0
    return True

def valid_battle(bo, ind, inf, num):
    # inf = ['battle', edge_list, dir, val]
    bo[ind[0]][ind[1]] = num
    sam = 0
    if bo[inf[1][0][0]][inf[1][0][1]] + bo[inf[1][8][0]][inf[1][8][1]] < 9:
        for k in range(bo[inf[1][0][0]][inf[1][0][1]],9-bo[inf[1][8][0]][inf[1][8][1]]):
            sam += bo[inf[1][k][0]][inf[1][k][1]]
    elif bo[inf[1][0][0]][inf[1][0][1]] + bo[inf[1][8][0]][inf[1][8][1]] > 9:
        for k in range(9-bo[inf[1][8][0]][inf[1][8][1]],bo[inf[1][0][0]][inf[1][0][1]]):
            sam += bo[inf[1][k][0]][inf[1][k][1]]  
    if inf[3] != sam:
        bo[ind[0]][ind[1]] = 0
        return False    
    bo[ind[0]][ind[1]] = 0
    return True
    
def valid_diag(bo, ind, inf, num):
    # inf = ['diag', ind_list, k]
    for k in range(9):
        if num == bo[inf[1][k][0]][inf[1][k][1]] and k != inf[2]:
            return False
    return True
    
def valid_thermo(bo, ind, inf, num):
    # inf = ['thermo', ind_list, k]
    if num < inf[2]:
        return False
    if inf[2] > 0 and num <= bo[inf[1][inf[2]-1][0]][inf[1][inf[2]-1][1]]: # check bigger than previous spot
        return False
    if inf[2] < (len(inf[1])-1) and bo[inf[1][inf[2]+1][0]][inf[1][inf[2]+1][1]] != 0 and num >= bo[inf[1][inf[2]+1][0]][inf[1][inf[2]+1][1]]:
        return False
    return True

def valid_pali(bo, ind, inf, num):
    # inf = ['pali', ind_list, k]
    if bo[inf[1][-(inf[2]+1)][0]][inf[1][-(inf[2]+1)][1]] != 0 and num != bo[inf[1][-(inf[2]+1)][0]][inf[1][-(inf[2]+1)][1]]:
        return False
    return True

def valid_killer(bo, ind, inf, num):
    # inf = [['little', ind_list, val]]
    for k in range(len(inf[1])):
        if bo[inf[1][k][0]][inf[1][k][1]] == num:
            return False
    return valid_little(bo, ind, inf, num)
    
def valid_little(bo, ind, inf, num):
    # inf = [['little', ind_list, val]]
    bo[ind[0]][ind[1]] = num
    sam = 0
    for k in range(len(inf[1])):
        sam += bo[inf[1][k][0]][inf[1][k][1]]
    if sam > inf[2]:
        bo[ind[0]][ind[1]] = 0
        return False
    if sam < inf[2] and not has_num(bo, inf[1], 0):
        bo[ind[0]][ind[1]] = 0
        return False
    if sam == inf[2] and has_num(bo, inf[1], 0):
        bo[ind[0]][ind[1]] = 0
        return False
    bo[ind[0]][ind[1]] = 0
    return True

def valid_circle(bo, ind, inf, num):
    # inf = ['circle', ind_list, num_list]
    bo[ind[0]][ind[1]] = num
    if not has_num(bo, inf[1], 0):
        seth = [bo[inf[1][k][0]][inf[1][k][1]] for k in range(len(inf[1]))]
        for i in range(len(inf[2])):
            if inf[2][1] not in seth:
                bo[ind[0]][ind[1]] = 0
                return False
    bo[ind[0]][ind[1]] = 0
    return True        

def valid_arrow(bo, ind, inf, num):
    # inf = ['arrow', ind_list, ind_val]
    bo[ind[0]][ind[1]] = num
    if not has_num(bo, inf[2], 0):
        vals = [bo[inf[2][t][0]][inf[2][t][1]] for t in range(len(inf[2]))]
        vlad = int("".join(([str(vals[k]) for k in range(len(vals))])))
        sam = 0
        for k in range(len(inf[1])):
            sam += bo[inf[1][k][0]][inf[1][k][1]]
        if sam > vlad:
            bo[ind[0]][ind[1]] = 0
            return False
        if sam < vlad and not has_num(bo, inf[1], 0):
            bo[ind[0]][ind[1]] = 0
            return False
        if sam == vlad and has_num(bo, inf[1], 0):
            bo[ind[0]][ind[1]] = 0
            return False
    bo[ind[0]][ind[1]] = 0
    return True

def valid_between(bo, ind, inf, num):
    # inf = ['between', ind_list, ind_edge]
    bo[ind[0]][ind[1]] = num
    if not has_num(bo, inf[2], 0):
        minnie = min(bo[inf[2][0][0]][inf[2][0][1]], bo[inf[2][1][0]][inf[2][1][1]])
        maxwell = max(bo[inf[2][0][0]][inf[2][0][1]], bo[inf[2][1][0]][inf[2][1][1]])
        for k in range(len(inf[1])):
            if bo[inf[1][k][0]][inf[1][k][1]] >= maxwell:
                bo[ind[0]][ind[1]] = 0
                return False
            if bo[inf[1][k][0]][inf[1][k][1]] <= minnie and bo[inf[1][k][0]][inf[1][k][1]] != 0:
                bo[ind[0]][ind[1]] = 0
                return False
    bo[ind[0]][ind[1]] = 0
    return True
    
def valid_odd(bo, ind, inf, num):
    # inf = ['odd']
    if (num % 2) == 0:
        return False
    return True

def valid_even(bo, ind, inf, num):
    # inf = ['odd']
    if (num % 2) == 1:
        return False
    return True

def valid_min(bo, ind, inf, num):
    # inf = ['min', ind_list] where num must be less than all nums in ind_list
    for k in range(len(inf[1])):
        if bo[inf[1][k][0]][inf[1][k][1]] != 0 and num > bo[inf[1][k][0]][inf[1][k][1]]:
            return False
    return True

def valid_max(bo, ind, inf, num):
    # inf = ['min', ind_list] where num must be more than all nums in ind_list
    for k in range(len(inf[1])):
        if num < bo[inf[1][k][0]][inf[1][k][1]]:
            return False
    return True

def valid_black(bo, ind, inf, num):
    # inf = ['black', ind_list, k_other, ratio]
    if bo[inf[1][inf[2]][0]][inf[1][inf[2]][1]]/num == inf[3] or bo[inf[1][inf[2]][0]][inf[1][inf[2]][1]]/num == 1/inf[3] or bo[inf[1][inf[2]][0]][inf[1][inf[2]][1]]/num == 0:
        return True
    return False

def valid_white(bo, ind, inf, num):
    # inf = ['white', ind_list, k_other, diff]
    if num-bo[inf[1][inf[2]][0]][inf[1][inf[2]][1]] == inf[3] or num-bo[inf[1][inf[2]][0]][inf[1][inf[2]][1]] == -inf[3] or num-bo[inf[1][inf[2]][0]][inf[1][inf[2]][1]] == num:
        return True
    return False

def valid_clone(bo, ind, inf, num):
    # inf = ['clone', other_ind]
    if bo[inf[1][0]][inf[1][1]] != 0 and bo[inf[1][0]][inf[1][1]] != num:
        return False
    return True
