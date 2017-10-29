# Astar.py, April 2017 
# Based on ItrDFS.py, Ver 0.4a, October 14, 2017.

# A* Search of a problem space.
# The Problem should be given in a separate Python
# file using the "QUIET" file format.
# See the TowerOfHanoi.py example file for details.
# Examples of Usage:

# A small change was made on Oct. 14, so that backtrace
# uses None as the BACKLINK value for the initial state,
# just as in ItrDFS.py, rather than using -1 as it did
# in an earlier version.

# python3 AStar.py EightPuzzleWithHeuristics h_manhattan
'''Astar.py
Karan Murthy, CSE 415, Autumn 2017, University of Washington
UWNetID: karan7
Instructor:  S. Tanimoto.
Assignment 3 Part II.  Question 3 and 4 (A-Star Implementation)
'''

import sys
from priorityq import PriorityQ

# DO NOT CHANGE THIS SECTION 
if sys.argv==[''] or len(sys.argv)<2:
    import Eradicate_Cold as Problem
    heuristics = lambda s: Problem.HEURISTICS['h_manhattan'](s)
    initial_state = Problem.CREATE_INITIAL_STATE()
else:
    import importlib
    Problem = importlib.import_module(sys.argv[1])
    heuristics = lambda s: Problem.HEURISTICS[sys.argv[2]](s)
    inputs = importlib.import_module(sys.argv[3].split('.')[0])
    initial_state = Problem.CREATE_INITIAL_STATE(inputs.population_count, inputs.sick_people_count)


print("\nWelcome to AStar")
COUNT = None
BACKLINKS = {}

# DO NOT CHANGE THIS SECTION
def runAStar():
    #initial_state = Problem.CREATE_INITIAL_STATE(keyVal)
    
    print("Initial State:")
    print(initial_state)
    global COUNT, BACKLINKS
    COUNT = 0
    BACKLINKS = {}
    path, name = AStar(initial_state)
    print(str(COUNT)+" states examined.")
    return path, name

# A star search algorithm
# TODO: finish A star implementation
def AStar(initial_state):
    global COUNT, BACKLINKS
    # TODO: initialze and put first state into 
    # priority queue with respective priority
    # add any auxiliary data structures as needed
    OPEN = PriorityQ()
    CLOSED = []
    GVALUE = {}
    FVALUE = {}
    BACKLINKS[initial_state] = None
    GVALUE[initial_state] = 0
    FVALUE[initial_state] = GVALUE[initial_state] + heuristics(initial_state)
    OPEN.insert(initial_state, FVALUE[initial_state])
      
    while not OPEN.isEmpty():
        S = OPEN.deletemin()
        while S in CLOSED:
            S = OPEN.deletemin()
        CLOSED.append(S)
        
        # DO NOT CHANGE THIS SECTION: begining 
        if Problem.GOAL_TEST(S):
            print(Problem.GOAL_MESSAGE_FUNCTION(S))
            path = backtrace(S)
            return path, Problem.PROBLEM_NAME
        # DO NOT CHANGE THIS SECTION: end

        # TODO: finish A* implementation
        COUNT += 1
        for op in Problem.OPERATORS:
          if op.precond(S):
            new_state = op.state_transf(S)
            if not occurs_in(new_state, CLOSED) and not OPEN.__contains__(new_state):
                GVALUE[new_state] = GVALUE[S] + 1
                FVALUE[new_state] = GVALUE[new_state] + heuristics(new_state)
                BACKLINKS[new_state] = S
                OPEN.insert(new_state, FVALUE[new_state])
            else:
                predecessor = BACKLINKS[new_state]
                # Check if we found a link to the initial node by chance.
                # This would be the case when predecessor is None.
                if predecessor is not None:     
                    heuristic_val = FVALUE[new_state] - GVALUE[predecessor] - 1
                    temp = heuristic_val + GVALUE[S] + 1
                    if temp < FVALUE[new_state]:
                        GVALUE[new_state] = GVALUE[new_state] - FVALUE[new_state] + temp
                        FVALUE[new_state] = temp
                        BACKLINKS[new_state] = S
                        if occurs_in(new_state, CLOSED):
                            CLOSED.remove(new_state)
                            OPEN.insert(new_state, FVALUE[new_state])
                
                

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

def occurs_in(s1, lst):
  for s2 in lst:
    if s1==s2: return True
  return False

if __name__=='__main__':
    path, name = runAStar()

