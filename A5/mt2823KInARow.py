'''
Meijing Tian, mt2823, CSE 415, Autumn 2017, University of Washington
Instructor:  S. Tanimoto.
Assignment 5 Part I. Option B. Individual Work and K-in-a-Row
'''

from copy import deepcopy
import math
import sys

K = 5
FORBID = list() # list of tuples
MYSIDE = ''
OPPOSIDE = ''
OPPONAME = ""

class State:
    def __init__(self, data):
        self.whosTurn = data[1]
        self.mat = data[0] # two d matrix
        self.rows = len(self.mat)
        self.cols = len(self.mat[0])

    def evalConsec(self, symbol):
        symbolInRows = dict()
        for i in range(self.rows):
            for j in range(self.cols):
                if self.mat[i][j] == symbol:
                                           
                    # check in the same row (consecutive)
                    consRow = False
                    leftFlg = False
                    if j > 0 and self.mat[i][j-1] == symbol:
                        leftFlg = True
                    if not leftFlg:
                        count = 1 
                        for col in range(j+1, self.cols):
                            if self.mat[i][col] == symbol:
                                #self.mat[i][col] = mask
                                consRow = True
                                count += 1
                            else:
                                break
                        if consRow:
                            if count not in symbolInRows:
                                symbolInRows[count] = 1
                            else:
                                symbolInRows[count] += 1
                    
                    # check in the same col (consecutive)
                    consCol = False
                    upFlg = False
                    if i > 0 and self.mat[i-1][j] == symbol:
                        upFlg = True
                    if not upFlg:
                        count = 1
                        for row in range(i+1, self.rows):
                            if self.mat[row][j] == symbol:
                                count += 1
                                consCol = True
                            else:
                                break
                        if consCol:  
                            if count not in symbolInRows:
                                symbolInRows[count] = 1
                            else:
                                symbolInRows[count] += 1
                    
                    # check in diagonal (consecutive)
                    consDiag = False
                    upLeftFlg = False
                    if i > 0 and j > 0 and self.mat[i-1][j-1] == symbol:
                        upLeftFlg = True
                    if not upLeftFlg:
                        count = 1
                        row = i
                        col = j
                        while row < self.rows-1 and col < self.cols-1:
                            if self.mat[row+1][col+1] == symbol:
                                count += 1
                                consDiag = True
                            else:
                                break
                            row += 1
                            col += 1
                        
                        if consDiag:
                            if count not in symbolInRows:
                                symbolInRows[count] = 1
                            else:
                                symbolInRows[count] += 1
                    
                    # check in anti-diagonal (consecutive)
                    consAnti = False
                    upRightFlg = False
                    if i > 0 and j < self.cols-1 and self.mat[i-1][j+1] == symbol:
                        upRightFlg = True
                    if not upRightFlg:
                        count = 1
                        row = i
                        col = j
                        while row < self.rows-1 and col > 0:
                            if self.mat[row+1][col-1] == symbol:
                                count += 1
                                consAnti = True
                            else:
                                break
                            row += 1
                            col -= 1
                            
                        if consAnti:
                            if count not in symbolInRows:
                                symbolInRows[count] = 1
                            else:
                                symbolInRows[count] += 1
                    
                    if not consRow and not consCol and not consDiag and not consAnti \
                    and not leftFlg and not upFlg and not upLeftFlg and not upRightFlg:
                        count = 1
                        if count not in symbolInRows:
                            symbolInRows[count] = 1
                        else:
                            symbolInRows[count] += 1
        
        score = 0
        for key in symbolInRows:
            score += key * key * symbolInRows[key]
        return score
        
    def evalCenter(self, symbol):
        midRow = (int) (self.rows / 2)
        midCol = (int) (self.cols / 2)
        totDist = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if self.mat[i][j] == symbol:
                    totDist += calcEuclideanDist((midRow, midCol), (i, j))
        return totDist
        
    def evalForbid(self, symbol):
        minDist = sys.maxsize
        for fPos in FORBID:
            totDist = 0
            for i in range(self.rows):
                for j in range(self.cols):
                    if self.mat[i][j] == symbol:
                        totDist += calcEuclideanDist(fPos, (i, j))
            if totDist < minDist:
                minDist = totDist
              
        if minDist == sys.maxsize:
            return 0
        return minDist 
        
        
    def evalState(self):

        myConsec = self.evalConsec(MYSIDE)
        oppoConsec = self.evalConsec(OPPOSIDE)
        myForbidDist = self.evalForbid(MYSIDE)
        oppoForbidDist = self.evalForbid(OPPOSIDE)
        myCenterSc = self.evalCenter(MYSIDE)
        oppoCenterSc = self.evalCenter(OPPOSIDE)
        
        myScore = myConsec + 0.5 * myForbidDist - 0.8 * myCenterSc
        oppoScore = oppoConsec + 0.5 * oppoForbidDist - 0.8 * oppoCenterSc

        diff = (myScore - oppoScore) / 5 # just to scale the score
        
        return (1 - math.exp(-diff)) / (1 + math.exp(-diff))

 
def calcEuclideanDist(fPos, symPos):
    forbidX = fPos[0]
    forbidY = fPos[1]
    symX = symPos[0]
    symY = symPos[1]
    return math.sqrt((forbidX - symX) * (forbidX - symX) + (forbidY - symY) * (forbidY - symY))

def prepare(initial_state, k, what_side_I_play, opponent_nickname):
    global K, FORBID, MYSIDE, OPPOSIDE, OPPONAME
    K = k
    MYSIDE = what_side_I_play
    if MYSIDE == 'X':
        OPPOSIDE = 'O'
    else:
        OPPOSIDE = 'X'
    OPPONAME = opponent_nickname
    initState = State(initial_state)
    for i in range(initState.rows):
        for j in range(initState.cols):
            if initState.mat[i][j] == '-':
                FORBID.append((i, j))
                

def introduce():
    intro = '''This is Alpha_MT_2. 
    I was created by Meijing Tian, mt2823. 
    I will claim victory / lose when I am sure of it.
    I will be honest sometime but I can also bluff!
    '''
    return intro

def nickname():
    return "Alpha_MT_2"


def isTerminal(currentState, symbol):
    mat = currentState[0]
    rows = len(mat)
    cols = len(mat[0])
    for i in range(rows):
        for j in range(cols):
            if mat[i][j] == symbol:
                count = 1
                for col in range(j+1, cols):
                    if mat[i][col] == symbol:
                        count += 1
                        if count == K:
                            return True
                    else:
                        break
                
                count = 1
                for row in range(i+1, rows):
                    if mat[row][j] == symbol:
                        count += 1
                        if count == K:
                            return True
                    else:
                        break
                
                count = 1
                row = i
                col = j
                while row < rows-1 and col < cols-1:
                    if mat[row+1][col+1] == symbol:
                        count += 1
                        if count == K:
                            return True
                    else:
                        break
                    row += 1
                    col += 1
                
                count = 1
                row = i
                col = j
                while row < rows-1 and col > 0:
                    if mat[row+1][col-1] == symbol:
                        count += 1
                        if count == K:
                            return True
                    else:
                        break
                    row += 1
                    col -= 1
    return False

    
   
def actions(currentState, move):
    mat = currentState[0]
    rows = len(mat)
    cols = len(mat[0])
    player = currentState[1]
    oppo = ''
    if player == 'X':
        oppo = 'O'
    else:
        oppo = 'X'
    res = list() # list of tuples (nextstate, move positon)
    for i in range(rows):
        for j in range(cols):
            if mat[i][j] == ' ':
                matCopy = deepcopy(mat)
                matCopy[i][j] = player
                moveCopy = deepcopy(move)
                moveCopy.append((i, j))
                res.append(([matCopy, oppo], moveCopy))
                

    return res

def makeMove(currentState, currentRemark, timeLimit=10000):
    thinkDepth = 2
    res = list()
    curMat = currentState[0]
    curPlayer = currentState[1]
    nxtPlayer = ''
    if curPlayer == MYSIDE:
        nxtPlayer = OPPOSIDE
    else:
        nxtPlayer = MYSIDE
    miniTup = miniMax((currentState, []), thinkDepth)
    judge = miniTup[0]
    nextMove = miniTup[1][0]
    newMat = deepcopy(curMat)
    newMat[nextMove[0]][nextMove[1]] = curPlayer
    newState = [newMat, nxtPlayer]
    newRemark = ""
    if judge == 1: 
        newRemark = "Yeah! I win for sure! Good play " + OPPONAME + "! Evaluation: " + str(judge * 100) + "%"
    elif judge > 0.75 and judge < 1:
        newRemark = "Current stage is good for me! Evaluation: " + str(judge * 100) + "%"
    elif judge >= 0.25 and judge <= 0.75:
        newRemark = "Hey " + OPPONAME + ", I can win in the next move! (Bluffing) Evaluation: " + str(judge * 100) + "%"
    elif judge < 0.25 and judge > -0.25:
        newRemark = "Hmmm... It's quite unclear... Evaluation: " + str(judge * 100) + "%"
    elif judge <= -0.25 and judge >= -0.75:
        newRemark = "Let's keep going. Who knows which one of us can win. (Bluffing) Evaluation: " + str(judge * 100) + "%"
    elif judge < -0.75 and judge > -1:
        newRemark = "Watch out " + OPPONAME + "! I still have a chance to win! (Bluffing) Evaluation: " + str(judge * 100) + "%"
    else:
        newRemark = "Oh! I lose for sure! Good play " + OPPONAME + "! Evaluation: " + str(judge * 100) + "%"
    
    res.append([nextMove, newState])
    res.append(newRemark)
    return res

def miniMax(currentStateTuple, depth):
    player = currentStateTuple[0][1]
    currentState = currentStateTuple[0]
    move = currentStateTuple[1]
    if depth == 0:
        return (staticEval(currentState), move)
    elif player == MYSIDE:
        nextStateTuples = actions(currentState, move)
        res = list()
        for nextStateTuple in nextStateTuples:
            if isTerminal(nextStateTuple[0], MYSIDE):
                return (1, nextStateTuple[1])
            
        for nextStateTuple in nextStateTuples:
            res.append(miniMax(nextStateTuple, depth-1))
        return max(res, key=lambda x : x[0])
    else:
        nextStateTuples = actions(currentState, move)
        res = list()
        for nextStateTuple in nextStateTuples:
            if isTerminal(nextStateTuple[0], OPPOSIDE):
                return (-1, nextStateTuple[1])
        for nextStateTuple in nextStateTuples:
            res.append(miniMax(nextStateTuple, depth-1))

        return min(res, key=lambda x : x[0])
    

def staticEval(state):
    stateObj = State(state)
    return stateObj.evalState()


