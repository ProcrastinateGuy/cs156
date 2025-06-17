from A2b_Base import *

#______DO NOT EDIT ABOVE THIS LINE____________#
#use deque functions to add and remove frontier entries
#______EDITING BELOW THIS LINE IS ALLOWED, ONLY EDIT THE INTERNAL IMPLEMENTATION OF THE FUNCTIONS ____________#

class AStarGraph(GraphProblem):
    #use this child class, Inherit from the GraphProblem class, in this class implement hueristic (h) function
    """h function is straight-line distance from a node's state to goal."""
    # in this case use the romania_map.locations attribute to compute h.
    def h(self, node):
        #YOUR CODE GOES HERE
#ok


def astar_search(problem, h=None):
    """A* search is best-first (you may use priority queue) graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, (ALREADY ADDED in TEST CASE),
    The tests check through a call to solution() function which returns a list of expanded cities along the path"""

    # YOUR CODE GOES HERE

