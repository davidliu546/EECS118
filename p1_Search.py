# p1_Search.py
# ---------
# Based on search.py from the UC Berkeley Pacman AI Projects.
# Original authors: John DeNero, Dan Klein, Brad Miller, Nick Hay, Pieter Abbeel.
# Original project link: http://ai.berkeley.edu
#
# Modifications for UCI EECS 118 by Mahmoud Elfar, 2025.
# This version includes changes to <TBD>.
#
# Licensing: You may use or extend this file for educational purposes
# provided that (1) solutions are not distributed or published,
# (2) this notice is retained, and (3) clear attribution to UC Berkeley is kept. test


"""
In p1_Search.py, you will implement generic search algorithms which are called by
Pacman agents (in p1_SearchAgents.py).
"""

import util
from util import Stack, Queue, PriorityQueue
from game import Directions
from typing import List

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # uses stack as data structure
    stack = Stack()
    start = problem.getStartState()
    stack.push((start, []))     # passing in tuple of state and action to frontier
    visited = set()             # for faster runtime, could use [] and .append when checking
    
    while not stack.isEmpty():
        # exploring
        state, actions = stack.pop()    

        if state in visited:
            continue
        visited.add(state)

        if problem.isGoalState(state):
            return actions
        
        # expanding the successors
        for successor, action, stepCost in problem.getSuccessors(state):
            if successor not in visited:
                new_actions = actions + [action]
                stack.push((successor, new_actions))    
    
    # no solution
    return[]
    
        
def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    # BFS uses queue instead of stack for its data structure, same process
    queue = Queue()
    start = problem.getStartState()
    queue.push((start, []))     
    visited = set()       
    
    while not queue.isEmpty():
        # exploring
        state, actions = queue.pop()    

        if state in visited:
            continue
        visited.add(state)

        if problem.isGoalState(state):
            return actions
        
        # expanding the successors
        for successor, action, stepCost in problem.getSuccessors(state):
            if successor not in visited:
                new_actions = actions + [action]
                queue.push((successor, new_actions))    
    
    # no solution
    return[]
    

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # Uses priority queue as data structure
    pq = PriorityQueue()
    start = problem.getStartState()
    pq.push((start, [], 0), 0)      # now adding overall cost as well as priority (lower cost = higher priority)
    visited = {}                    # mapping cost, use dict.      
    
    while not pq.isEmpty():
        # exploring
        state, actions, totalCost = pq.pop()    

        # skip if visited state before at cheaper cost than popped node
        if state in visited and visited[state] <= totalCost:
            continue

        if problem.isGoalState(state):
            return actions
        
        # record best cost to reach curr_state
        visited[state] = totalCost

        # expanding the successors
        for successor, action, stepCost in problem.getSuccessors(state):
            newCost = totalCost + stepCost
            new_actions = actions + [action]
            # update priority based on exisiting costs
            pq.update((successor, new_actions, newCost), newCost)       
    
    # no solution
    return[]


def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    """ uses both cost and heuristic to determine priority """
    start = problem.getStartState()
    pq = PriorityQueue()
    pq.push((start, [], 0), heuristic(start, problem))  # state, actions, totalCost, heuristic
    
    cost = {start: 0}  # mapping cost to reach each state   

    while not pq.isEmpty():
        state, actions, totalCost = pq.pop()

        if problem.isGoalState(state):
            return actions
        
        # expanding the successors
        for successor, action, stepCost in problem.getSuccessors(state):
            newCost = totalCost + stepCost
            # only if never visited or found cheaper path to successor
            if successor not in cost or newCost < cost[successor]:
                cost[successor] = newCost
                new_actions = actions + [action]
                new_heuristic = newCost + heuristic(successor, problem)
                pq.update((successor, new_actions, newCost), new_heuristic)
            
    # no solution
    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
