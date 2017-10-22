'''EightPuzzleWithHeuristics.py
Aman Arya
aarya22
#1535134

A QUIET2 Solving Tool problem formulation.
QUIET = Quetzal User Intelligence Enhancing Technology.
The XML-like tags used here serve to identify key sections of this
problem formulation.  It is important that COMMON_CODE come
before all the other sections (except METADATA), including COMMON_DATA.
CAPITALIZED constructs are generally present in any problem
formulation and therefore need to be spelled exactly the way they are.
Other globals begin with a capital letter but otherwise are lower
case or camel case.
'''
# <METADATA>
QUIET_VERSION = "0.2"
PROBLEM_NAME = "Eight Puzzle with Heuristics"
PROBLEM_VERSION = "0.2"
PROBLEM_AUTHORS = ['Aman Arya']
PROBLEM_CREATION_DATE = "15-OCT-2017"
PROBLEM_DESC = \
    '''This formulation of the Basic Eight Puzzle problem uses generic
    Python 3 constructs and has been tested with Python 3.6.
    It is designed to work according to the QUIET2 tools interface.
    '''


# </METADATA>
import math

# <COMMON_CODE>
class State:
    def __init__(self, d):
        self.d = d

    def __eq__(self, s):
        for i in range(9):
            if s.d[i] != self.d[i]:
                return False
        return True

    def __str__(self):
        # Produces a textual description of a state.
        # Might not be needed in normal operation with GUIs.
        return str(self.d)

    def __hash__(self):
        return (self.__str__()).__hash__()

    def copy(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        news = State(list(self.d))
        return news

    def can_move(self, mnum):
        '''Tests whether it's legal to move with mnum'''
        try:
            idx = self.d.index(0)
            if idx + mnum < 0 or idx + mnum > 8:
                return False
            if idx % 3 == 0 and mnum == -1:
                return False
            if idx % 3 == 2 and mnum == 1:
                return False
            return True

        except (Exception) as e:
            print(e)

    def move(self, mnum):
        '''Makes the move by mnum if possible '''
        news = self.copy()
        empty = self.d.index(0)
        news.d[empty] = self.d[empty+mnum]
        news.d[empty+mnum] = 0
        return news


def goal_test(s):
    '''Checks if state matches goal state'''
    return s.d == [0, 1, 2, 3, 4, 5, 6, 7, 8]


def goal_message(s):
    return "Solved the 8 puzzle."


def h_euclidean(s):
    s = s.d
    r = 0
    goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    for i in s:
        idx = s.index(i)
        gidx = goal.index(i)
        row = idx / 3
        col = idx % 3
        grow = gidx / 3
        gcol = gidx % 3
        r += math.sqrt(math.pow((grow-row), 2) + math.pow((gcol-col), 2))
    return r


def h_hamming(s):
    s = s.d
    r = 0
    goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    for i in s:
        if s.index(i) != goal.index(i):
            r += 1
    return r


def h_manhattan(s):
    s = s.d
    r = 0
    goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    for i in s:
        idx = s.index(i)
        gidx = goal.index(i)
        row = idx / 3
        col = idx % 3
        grow = gidx / 3
        gcol = gidx % 3
        r += abs(grow + row) + abs(gcol+col)
    return r


def h_custom(s):
    # Equivalent to octile distance
    s = s.d
    D = 1
    D2 = math.sqrt(2)
    r = 0
    goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    for i in s:
        idx = s.index(i)
        gidx = goal.index(i)
        row = idx / 3
        col = idx % 3
        grow = gidx / 3
        gcol = gidx % 3
        dx = abs(row - grow)
        dy = abs(col - gcol)
        r += D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
    return r

class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)


# </COMMON_CODE>

# <INITIAL_STATE>
# puzzle 0
# CREATE_INITIAL_STATE = lambda: State([0, 1, 2, 3, 4, 5, 6, 7, 8])
# puzzle 1
# CREATE_INITIAL_STATE = lambda: State([1, 0, 2, 3, 4, 5, 6, 7, 8])
# puzzle 2
# CREATE_INITIAL_STATE = lambda: State([3, 1, 2, 4, 0, 5, 6, 7, 8])
# puzzle 3
# CREATE_INITIAL_STATE = lambda: State([1, 4, 2, 3, 7, 0, 6, 8, 5])
# puzzle 10
# CREATE_INITIAL_STATE = lambda: State([4, 5, 0, 1, 2, 3, 6, 7, 8])
# puzzle 12
# CREATE_INITIAL_STATE = lambda: State([3, 1, 2, 6, 8, 7, 5, 4, 0])
# puzzle 14
# CREATE_INITIAL_STATE = lambda: State([4, 5, 0, 1, 2, 8, 3, 7, 6])
# puzzle 16
CREATE_INITIAL_STATE = lambda: State([0, 8, 2, 1, 7, 4, 3, 6, 5])
# </INITIAL_STATE>

# <OPERATORS>
possible = [-3, -1, 1, 3]
OPERATORS = [Operator("Move " + str(i),
                      lambda s, i1=i: s.can_move(i1),
                      # The default value construct is needed
                      # here to capture the values of p&q separately
                      # in each iteration of the list comp. iteration.
                      lambda s, i1=i: s.move(i1))
             for i in possible]
# </OPERATORS>

# <GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
# </GOAL_TEST>

# <GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
# </GOAL_MESSAGE_FUNCTION>

HEURISTICS = {'h_euclidean': h_euclidean, 'h_hamming':h_hamming,
    'h_manhattan':h_manhattan, 'h_custom':h_custom}
