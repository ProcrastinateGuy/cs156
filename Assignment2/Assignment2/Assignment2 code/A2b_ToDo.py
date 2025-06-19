from A2b_Base import *

#______DO NOT EDIT ABOVE THIS LINE____________#
#use deque functions to add and remove frontier entries
#______EDITING BELOW THIS LINE IS ALLOWED, ONLY EDIT THE INTERNAL IMPLEMENTATION OF THE FUNCTIONS ____________#

class AStarGraph(GraphProblem):
    import math
    #use this child class, Inherit from the GraphProblem class, in this class implement hueristic (h) function
    """h function is straight-line distance from a node's state to goal."""
    # in this case use the romania_map.locations attribute to compute h.
    def h(self, node):
        location_s = self.graph.locations.get(node)
        location_g = self.graph.locations.get(self.goal)
        distance = self.math.sqrt( ((location_s[0] - location_g[0]) ** 2 ) + ((location_s[1] - location_g[1]) ** 2 ))
        return self.math.trunc(distance)



def astar_search(problem, h=None):
    """A* search is best-first (you may use priority queue) graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, (ALREADY ADDED in TEST CASE),
    The tests check through a call to solution() function which returns a list of expanded cities along the path"""
    from queue import PriorityQueue
    import math
    from queue import PriorityQueue
    initial = Node(problem.initial)
    ori_nodes = problem.graph.nodes()

    explored = [] # keep track of the explored nodes
    score = {} # keep track of the current ASTAR score of that node

    # keep track of the branch that is actively expanding
    active_branch = PriorityQueue()

    nodes = {} # a different representation of the nodes in graph
    # dictionary, key = nodes obj, value = [heuristic, estimate]
    [nodes.update({ Node(x): [problem.h(x), math.inf] }) for x in ori_nodes]


    def get_cost(node):
        return nodes.get(node)[1]

    def set_cost(node, value):
        nodes.get(node)[1] = value

    def grab_children(node):
        return [ele for ele in node.expand(problem) if ele not in explored]

    # set the initial distance to 0
    set_cost(initial, 0)

    # put the initial to the explored, and record the score
    explored.append(initial)
    score.update( {initial: get_cost(initial)})

    def expand_tree(node):

        children = grab_children(node)
        # expand the node's neighbors into active branch
        for child in children:
            path_cost = get_cost(node) + problem.graph.get(node.state, child.state)
            estimate =  path_cost + problem.h(child.state) # path cost + heuristic

            # if the new estimate if better
            if (child not in score) or (estimate < score.get(child)):
                score.update({child: estimate}) # update the score of that node
            else: continue

            set_cost(child, path_cost) # update the path cost to that node

            pq_item = (estimate, child)
            active_branch.put(pq_item)


            if all(i for i in children) and active_branch.queue[0][1] == node:
                active_branch.get()


    expand_tree(initial)
    while active_branch.queue[0][1].state != problem.goal: # while the best branch is not the goal
        expand_tree(active_branch.queue[0][1]) # expand on the best branch
        """ debugging purposes
        print (f'score: {score}')
        print(f'nodes: {nodes}')
        print(f'active_branch: {[x for x in active_branch.queue]}')
        print(f'explored: {explored}')
        """
    return active_branch.queue[0][1]

