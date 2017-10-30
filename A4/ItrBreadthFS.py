"""
Aman Arya
aarya22
#1535134
"""
# ItrBreadthFS.py, Mar 2017
# Based on ItrDFS.py, Ver 0.4, Oct, 2017.

# Iterative Breadth-First Search of a problem space.
# The Problem should be given in a separate Python
# file using the "QUIET" file format.
# See the TowerOfHanoi.py example file for details.
# Examples of Usage:
# python3 ItrBreadthFS.py TowersOfHanoi
# python3 ItrBreadthFS.py EightPuzzle

import sys

if sys.argv==[''] or len(sys.argv)<2:
  #import BasicEightPuzzle as Problem
  #import TowerOfHanoi as Problem
   import person as Problem
else:
  import importlib
  Problem = importlib.import_module(sys.argv[1])


print("\nWelcome to ItrBFS")
COUNT = None
BACKLINKS = {}

#DO NOT CHANGE THIS FUNCTION
def runBFS(): 
  initial_state = Problem.CREATE_INITIAL_STATE()
  print("Initial State:")
  print(initial_state)
  global COUNT, BACKLINKS
  COUNT = 0
  BACKLINKS = {}
  path, name = IterativeBFS(initial_state)
  print(str(COUNT)+" states examined.")
  return path, name

# DO NOT CHANGE THE NAME OR THE RETURN VALUES
# TODO: implement the core BFS algorithm
def IterativeBFS(initial_state):
    global COUNT, BACKLINKS

    OPEN = [initial_state]
    CLOSED = []
    BACKLINKS[initial_state] = None

    while OPEN != []:
        S = OPEN.pop(0)
        CLOSED.append(S)

        # DO NOT CHANGE THIS SECTION
        # the goal test, return path if reached goal
        if Problem.GOAL_TEST(S):
            print("\n"+Problem.GOAL_MESSAGE_FUNCTION(S))
            backtrace(S)
            path = backtrace(S)
            return path, Problem.PROBLEM_NAME

        # DO NOT CHANGE THE CODE ABOVE 
        
        # TODO: finish BFS implementation

        COUNT += 1
        if True:
            print("COUNT = "+str(COUNT))
            print("len(OPEN)="+str(len(OPEN)))
            print("len(CLOSED)="+str(len(CLOSED)))

        L = []
        for op in Problem.OPERATORS:
            if op.precond(S):
                new_state = op.state_transf(S)
                if new_state not in CLOSED and new_state not in OPEN:
                    L.append(new_state)
                    BACKLINKS[new_state] = S

        L = [item for item in L if item not in CLOSED]
        L = [item for item in L if item not in OPEN]

        OPEN = OPEN + L
        print_state_list("OPEN", OPEN)

def print_state_list(name, lst):
    print(name + " is now: ", end='')
    for s in lst[:-1]:
        print(str(s), end=', ')
    print(str(lst[-1]))

# returns a list of states
# DO NOT CHANGE
def backtrace(S):
  global BACKLINKS
  path = [] 
  while S:
    path.append(S)
    S = BACKLINKS[S]
  path.reverse()
  print("Solution path: ")
  for s in path:
    print(s)
  print("\nPath length = "+str(len(path)-1))
  return path

if __name__=='__main__':
  path, name = runBFS()

"""
When ran on TowerOfHanoi

The Tower Transport is Triumphant!
Solution path:
[[4, 3, 2, 1] ,[] ,[]]
[[4, 3, 2] ,[1] ,[]]
[[4, 3] ,[1] ,[2]]
[[4, 3] ,[] ,[2, 1]]
[[4] ,[3] ,[2, 1]]
[[4, 1] ,[3] ,[2]]
[[4, 1] ,[3, 2] ,[]]
[[4] ,[3, 2, 1] ,[]]
[[] ,[3, 2, 1] ,[4]]
[[] ,[3, 2] ,[4, 1]]
[[2] ,[3] ,[4, 1]]
[[2, 1] ,[3] ,[4]]
[[2, 1] ,[] ,[4, 3]]
[[2] ,[1] ,[4, 3]]
[[] ,[1] ,[4, 3, 2]]
[[] ,[] ,[4, 3, 2, 1]]

Path length = 15
Solution path:
[[4, 3, 2, 1] ,[] ,[]]
[[4, 3, 2] ,[1] ,[]]
[[4, 3] ,[1] ,[2]]
[[4, 3] ,[] ,[2, 1]]
[[4] ,[3] ,[2, 1]]
[[4, 1] ,[3] ,[2]]
[[4, 1] ,[3, 2] ,[]]
[[4] ,[3, 2, 1] ,[]]
[[] ,[3, 2, 1] ,[4]]
[[] ,[3, 2] ,[4, 1]]
[[2] ,[3] ,[4, 1]]
[[2, 1] ,[3] ,[4]]
[[2, 1] ,[] ,[4, 3]]
[[2] ,[1] ,[4, 3]]
[[] ,[1] ,[4, 3, 2]]
[[] ,[] ,[4, 3, 2, 1]]

Path length = 15
70 states examined.
"""

"""
When ran on BasicEightPuzzle

puzzle0: solved, 0 states examined

puzzle1a: solved, 1 states examined

puzzle2a: solved, 7 states examined

puzzle4a: solved, 53 states examined
"""
