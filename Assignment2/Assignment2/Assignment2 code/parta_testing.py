from A2a_Base import *
from A2a_ToDo import *

problem = GraphProblem('Arad', 'Bucharest', romania_map)


# base case
node = Node(problem.initial) # the initial state

print(f'node = {node}')
frontier = deque([node])
explored = set() # a set to store the explored nodes

for child_node in problem.actions(str(node.state)):
    frontier.appendleft(child_node)

node_list = problem.graph.nodes()
print(node_list)

print(node.expand(problem))
pass