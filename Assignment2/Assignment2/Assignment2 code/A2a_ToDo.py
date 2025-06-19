from A2a_Base import *

#______DO NOT EDIT ABOVE THIS LINE____________#

#use deque functions to add and remove frontier entries


#______EDITING BELOW THIS LINE IS ALLOWED, ONLY EDIT THE INTERNAL IMPLEMENTATION OF THE FUNCTIONS ____________#
# returns a node
def breadth_first_graph_search(problem):
    """
    Implement the breadth first search for the graph here.
    some skeleton code is provided, feel free to edit it.
    Search through the successors/actions of a problem to find a goal.
    The initial frontier should be an empty queue.
    Does not get trapped by loops.
    If two paths reach a state, only use the first one.
    """

    # base case
    node = Node(problem.initial) # the initial state

    #goal test for root
    if problem.goal_test(node.state):
        return node

    # if the current node is not the goal state
    # create a dequeue to start the BFS
    frontier = deque(node.expand(problem)) # stuff the children of node into frontier

    explored = [node] # a list to store the explored nodes

    while frontier:
        # check if current level nodes are the goal
        current_frontier = list(frontier) # duplicate the frontier
        for node in frontier:
            if problem.goal_test(node.state):
                return node
            else:
                explored.append(node) # add the node to visited

        # add all their children to the frontier
        for node in current_frontier:
            neighbors = [ ele for ele in node.expand(problem) if ele not in frontier and ele not in explored ]
            frontier.extend(neighbors)
            frontier.remove(node) # pop the node once its children is added

    return None



def depth_first_graph_search(problem):
    """
    Search the deepest nodes in the search tree first.
    Search through the successors/actions of a problem to find a goal.
    The initial frontier should be an empty queue.
    Does not get trapped by loops.
    If two paths reach a state, only use the first one.
    """
    frontier = [(Node(problem.initial))]  # Stack
    explored = [(Node(problem.initial))]
    while frontier:
        top_element = frontier[-1]
        if problem.goal_test(top_element.state): # the top element
            return top_element
        else:
            # get the child list
            child = [ ele for ele in top_element.expand(problem) if ele not in frontier and ele not in explored ]

            if child is None or not child : # that means we have hit a leaf
                explored.append(top_element) # add the top into explored
                frontier.pop() # pop the top element
            else:
                frontier.extend(child) # add the child of the top to frontier


    return None


