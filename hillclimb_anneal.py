# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 20:46:24 2018

@author: Dean Shannon
"""

import random
import time

class Queen:
    x = 0
    y = 0
    def __init__(self, i, j):
        self.x = i
        self.y = j
        
class Successor:
    i = 0
    cost = 0
    def __init__(self, i, j):
        self.i = i
        self.cost = j
        
size = 32
maxPrintSize = 32
equalityThreshold = 3
startTemp = 1
queens = []
for i in range(size):
    queens.append(Queen(i, random.randint(0, size-1)))


def GetDifference(i, j):
    r = i - j
    if r < 0:
        r = r * (-1)
    return r

def IsAttacking(q1, q2):
    if q1 == q2:
        return False
    return (q1.x == q2.x or q1.y == q2.y or (GetDifference(q1.x, q2.x) == GetDifference(q1.y, q2.y)))
    

def GetCost(qlist):
    cost = 0
    for q in qlist:
        for q1 in qlist:
            if IsAttacking(q, q1):
                #print("("+str(q.x)+","+str(q.y)+") attacking "+"("+str(q1.x)+","+str(q1.y)+")")
                cost = cost + 1
    return cost

def IsQueen(qlist, x, y):
    for q in qlist:
        if q.x == x and q.y == y:
            return True
    return False

def MoveQueen(q, qlist, x, y):
    for o in qlist:
        if o.x == q.x and o.y == q.y:
            o.x = x
            o.y = y
    

def Climb(qlist, size, r):
    for q in qlist:
        options = []
        #lastX = q.x
        #lastY = q.y
        #print("FOR: "+str(q.x)+", "+str(q.y))
        for i in range(size):
            MoveQueen(q, qlist, q.x, i)
            cost = GetCost(qlist)
            #print("cost "+str(cost))
            #PrintBoard(qlist)
            options.append(Successor(i, cost))
            #MoveQueen(q, qlist, lastX, lastY)
        choice = Successor(-1, GetCost(qlist))
        #print("current cost: "+str(choice.cost))
        for o in options:
            #print("option cost: "+str(o.cost))
            if o.cost < choice.cost:
                choice = o
                #print("CHOSEN: "+str(choice))
        if choice.i > -1:
            #print(str(q.x)+", "+str(q.y)+" to "+str(q.x)+", "+str(choice.i))
            MoveQueen(q, qlist, q.x, choice.i)
            #print("FINAL CHOICE FOR COLUMN "+str(q.x))
            #PrintBoard(qlist)
   # print("Final Cost: "+str(GetCost(qlist)))
   # PrintBoard(qlist)
    return qlist

def Anneal(qlist, size, maxtime):
    time = 1
    while time < maxtime:
        for q in qlist:
            temp = Cool(time / maxtime)
            if temp == 0:
                return qlist
            new = random.randint(0, size-1)
            prevcost = GetCost(qlist)
            prevY = q.y
            #print(new)
            MoveQueen(q, qlist, q.x, new)
            newcost = GetCost(qlist)
            change = prevcost - newcost
            if change >= 0:
               #print("ACCEPTING...")
                time = time
            else:
                #print(change / temp)
                r = random.random()*-1
                #print(r)
                if r < (change / temp):
                    time = time
                   # print("ACCEPTING...")
                else:
                    MoveQueen(q, qlist, q.x, prevY)
                    #print("REVERTING...")
                    #revert move
           # print("Time: "+str(time)+", Temp: "+str(temp)+", Cost: "+str(newcost)+", Change: "+str(change))
        time = time + 1
    return qlist
        
def Cool(t):
    return startTemp - t * startTemp
                
            
    

def PrintBoard(qlist):
    if size <= maxPrintSize:
        for i in range(size):
            for j in range(size):
                isq = False
                for q in qlist:
                    if(q.x == j and q.y == i):
                        isq = True
                if isq:
                    print("[x]", end = "", flush = True)
                else:
                    print("[ ]", end = "", flush = True)
            print("")
        

#PrintBoard(queens)
#PrintBoard(queens)   
print("Board Size: "+str(size)+", Starting Temperature: "+str(startTemp)+", Equality Threshold: "+str(equalityThreshold))
print("Original Cost: "+str(GetCost(queens)))   
PrintBoard(queens)
startTime = time.clock()
currentcost = GetCost(Anneal(queens, size, (25 + size * 1.75)))
equality = 0
while (currentcost > 0):
    lastcost = currentcost
    startTemp = startTemp / 2
    currentcost = GetCost(Anneal(queens, size, (25 + size * 1.75)))
    print("Current Cost: "+str(currentcost))
    if lastcost <= currentcost:
        equality = equality + 1
    else:
        equality = 0
    if equality >= equalityThreshold:
        break
print("Final Cost: "+str(currentcost))
calcTime = time.clock() - startTime    
PrintBoard(queens)
if currentcost > 0:
    print("- FAILED")
else:
    print("+ PASSED")
print("algorithm executed in "+str(calcTime)+" seconds ("+str(time.clock() - (startTime + calcTime))+" sec/s taken to print board)")

                