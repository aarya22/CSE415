import time
from random import randint, choice
from numpy import zeros

K = 0
length = 0
width = 0
board = []
opponent = ""
side_I_play = ''
rows_flag = 0
cols_flag = 0
leftup_diagonal = []
rightup_diagonal = []
diffsign = {'O':'X', 'X':'O'}

winRemark = ["Ah ha! I win!", "Well played, let's have another game after you get stronger.", "Don't give up. Try Again."]
prewinRemark = ["Haha.", "The Light shall bring victory!", "Are you sure you want that move?"]
normalRemark = ["Hmmm... ", "I will beat you. ", "Let me think..."]
loseRemark = ["The victory is yours, but I'll be back.", "You win... this time.", "I concede to you."]
negtiRemark = ["Not quite what was planned.", "That was a mistake."]

def prepare(initial_state, k, what_side_I_play, opponent_nickname):
    global width, length, opponent, side_I_play, board, rows_flag, cols_flag, lslant, rslant, K
    board = initial_state[0]
    width = len(board[0])
    length = len(board)
    K = k
    flag = 0
    opponent = opponent_nickname
    side_I_play = what_side_I_play
    if k <= width: rows_flag = 1
    if k <= length: cols_flag = 1
    if rows_flag == 1 and cols_flag == 1:
        for i in range(length-k+1):
            leftup_diagonal.append([i, 0])
            rightup_diagonal.append([i, width-1])
        for i in range(width-k+1):
            leftup_diagonal.append([0, i])
        for i in range(k-1, width):
            rightup_diagonal.append([0, i])
    if leftup_diagonal.count([0,0]) == 2:
        leftup_diagonal.remove([0,0])
    if rightup_diagonal.count([0, width-1]) == 2:
        rightup_diagonal.remove([0, width-1])


def introduce():
	return """
    My name is Antoki. I am a K-in-a-row player.
    I have confidence to beat every opponent I meet within this game.
    My creator is Ching Lu and his NetID is tony 1023."""

def nickname():
	return "Antoki"

def makeMove(currentState, currentRemark, timeLimit=10000):
    global side_I_play, K, length, width, winRemark, prewinRemark, normalRemark, loseRemark, negtiRemark
    timeWhenStart = time.time()
    score, newState = minimax(currentState, timeLimit, timeWhenStart, 2)
    score_board = [10**i for i in range(K)]

    newRemark = ""
    if  score > score_board[-1] - score_board[-2]:
        newRemark = choice(winRemark)
    elif score > 3*score_board[-2]:
        newRemark = choice(prewinRemark)
    elif score < -score_board[-1] + score_board[-2]:
        newRemark = choice(loseRemark)
    elif score < 0:
        newRemark = choice(negtiRemark)
    else:
        newRemark = choice(normalRemark)

    for row in range(length):
        if currentState[0][row] != newState[0][row]:
            for col in range(width):
                if currentState[0][row][col] != newState[0][row][col]:
                    return [[[row, col], newState], newRemark]

def staticEval(state):
    global length, width, side_I_play, K, rows_flag, cols_flag, leftup_diagonal, rightup_diagonal
    score = 0
    score_board = [10**i for i in range(K)]
    my_distribution = list(zeros(K))
    op_distribution = list(zeros(K))
    if rows_flag == 1:
        for i in range(length):
            row = state[0][i]
            scan_board(row, my_distribution, op_distribution)
    if cols_flag == 1:
        for i in range(width):
            col = []
            for j in range(length):
                col.append(state[0][j][i])
            scan_board(col, my_distribution, op_distribution)
    increase = 0
    for i in leftup_diagonal:
        tmp_list = []
        while i[0]+increase <= length-1 and i[1]+increase <= width-1:
            tmp_list.append(state[0][i[0]+increase][i[1]+increase])
            increase += 1
        scan_board(tmp_list, my_distribution, op_distribution)
    increase = 0
    for i in rightup_diagonal:
        tmp_list = []
        while i[0]+increase <= length-1 and i[1]-increase >= 0:
            tmp_list.append(state[0][i[0]+increase][i[1]-increase])
            increase += 1
        scan_board(tmp_list, my_distribution, op_distribution)
    for i in range(K):
        score += score_board[i] * (my_distribution[i] - op_distribution[i])
    return score

def minimax(state, timeLimit, timeStart, plyLeft):
    global side_I_play, K, diffsign
    if (plyLeft == 0):
        return [staticEval(state), state]
    if state[1] == side_I_play:
        provisional = -100000
    else:
        provisional = 100000
    if time.time() - timeStart >= timeLimit*0.8:
        return [staticEval(state), state]

    # successors
    L = []
    for r in range(length):
        for c in range(width):
            if state[0][r][c] == ' ':
                tmp = copy(state[0])
                tmp[r][c] = state[1]
                L.append([tmp, diffsign[state[1]]])

    for s in L:
        newVal, tmpstate = minimax(s, timeLimit, timeStart, plyLeft - 1)
        if (state[1] == side_I_play and newVal > provisional) or (state[1] == diffsign[side_I_play] and newVal < provisional):
            provisional = newVal
            nextState = s
    return [provisional, nextState]

def scan_board(List, my_distribution, op_distribution):
    global side_I_play, K, diffsign
    me = [[], []] #[real, possible...]
    op = [[], []] #[real, possible...]
    tmp_op = 0
    tmp_me = 0
    real_op = 0
    real_me = 0
    winning = 0
    losing = 0
    count = 0
    # my side
    flag = 0
    for i in List:
        if i == side_I_play:
            flag = 1
            tmp_me += 1
            real_me += 1
            count += 1
        elif i == ' ':
            tmp_me += 1
            count = 0
        elif i == diffsign[side_I_play]:
            if real_me != 0: me[0].append(real_me)
            if tmp_me != 0 and flag == 1: me[1].append(tmp_me)
            tmp_me, real_me, flag, count = 0, 0, 0, 0
    if tmp_me != 0 and flag == 1: me[1].append(tmp_me)
    if real_me != 0: me[0].append(real_me)
    if count == K: winning = 1
    # op side
    flag, count = 0, 0
    for i in List:
        if i == diffsign[side_I_play]:
            flag = 1
            tmp_op += 1
            real_op += 1
            count += 1
        elif i == ' ':
            tmp_op += 1
            count = 0
        elif i == side_I_play:
            if real_op != 0: op[0].append(real_op)
            if tmp_op != 0 and flag == 1: op[1].append(tmp_op)
            tmp_op, real_op, flag, count = 0, 0, 0, 0
    if tmp_op != 0 and flag == 1: op[1].append(tmp_op)
    if real_op != 0: op[0].append(real_op)
    if count == K: losing = 1
    for i in range(len(me[1])):
        if me[1][i] >= K:
            if me[0][i] > K: my_distribution[-1] += 1
            else: my_distribution[me[0][i] - 1] += 1
    for i in range(len(op[1])):
        if op[1][i] >= K:
            if op[0][i] > K: op_distribution[-1] += 1
            else:
                if op[0][i] != 5: op_distribution[op[0][i]] += 1
                else: op_distribution[-1] += 1
    if winning == 1: my_distribution[-1] += 1
    if losing == 1: op_distribution[-1] += 1

def copy(board):
    tmp = []
    for i in board:
        tmps = []
        for j in i:
            tmps.append(j)
        tmp.append(tmps)
    return tmp

