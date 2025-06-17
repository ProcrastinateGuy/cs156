import math
import sys
from typing import List
# a Bellman-Ford implementation
# Student ID: 017837495
# Student name: shih-ru Sheng
# Date: Jun 9. 2025

# we need
# - an adjacency matrix
# - a list that stores the current shortest path for all the nodes
# - a way to input edges and vertices

# edges should include
# starting & ending vertex
# weight

# vertex should include
# label of the vertex

# e_tup is a tuple of lists
# an element in e_tup would be like
# [starting_V, weight, ending_V]

# v_tup is only a tuple of labels for the vertices.
# an element in v_tup would be like
# (a)

def print_adj_matrix(adj_matrix, num_v, v_tup) -> None:
    print('--------Graph As ADJ Matrix--------')
    print('    ' + ' '.join(f'{i:^3}' for i in v_tup))
    for i in range(num_v):
        print(f'{v_tup[i]:^3}', end = ' ')
        for j in range(num_v):
            print( f'{adj_matrix[i][j]:^3}', end = ' ')
        print()

def make_graph(num_v, num_e, v_tup, e_tup) -> List[ List[float] ]:
    # set all values to be infinity
    adj_matrix = [[ math.inf for _ in range(num_v)] for _ in range(num_v)]
    # set all self-distance to 0
    for i in range(num_v):
        adj_matrix[i][i] = 0

    # map the edges into the adj_matrix
    # - map the label to adj_matrix index
    vert_ind_transform = { label: index for index, label in enumerate(v_tup)}
    for i in range(len(e_tup)):
        # convert the vertex labels into indices
        # 0: starting index, 2: ending index
        e_tup[i][0] = vert_ind_transform.get(e_tup[i][0])
        e_tup[i][2] = vert_ind_transform.get(e_tup[i][2])

    # testing:
    # print(e_tup)
    # Ex. output: ([0, 4, 1], [1, 5, 2], [2, 6, 3], [3, 7, 4])

    # update the value of edges onto the adj_matrix
    for i in range(len(e_tup)):
        #adj_matrix: row: starting vertex
        #            column: ending vertex
        adj_matrix[e_tup[i][0]][e_tup[i][2]] = e_tup[i][1]


    # call the print matrix function to test
    print_adj_matrix(adj_matrix, num_v, v_tup)

    return adj_matrix


def relaxation(shortest_path, shortest_path_matrix, adj_matrix, edge):
    current_start = shortest_path_matrix[edge[0]]
    current_end = shortest_path_matrix[edge[2]]

    if ( current_start + edge[1] < current_end):
        shortest_path_matrix[edge[2]] = current_start + edge[1]
        # if relaxation happens, then update the shortest_path
        shortest_path[edge[2]] = list(shortest_path[edge[0]]) + [str(edge[2])]

def print_shortest_path(shortest_path, num_to_label, v_tup) -> None:

    print('--------Shortest Path--------')
    for i in range( len(shortest_path)):
        # index to label conversion
        shortest_path[i] = [num_to_label.get(x) for x in shortest_path[i]]
        # formatting the output
        shortest_path[i] = ' -> '.join(shortest_path[i])
        print(f's to {num_to_label.get(str(i))}: {shortest_path[i]}')

def print_shortest_path_matrix(shortest_path_matrix, num_to_label) -> None:
    print('--------Shortest Distance--------')
    for i in range( len(shortest_path_matrix)):
        # formatting the output
        print(f's to {num_to_label.get(str(i))}: {shortest_path_matrix[i]}')


# the main program
if __name__ == "__main__":

    # default value provided in assignment1
    num_v = 7
    num_e = 11
    v_tup = ('s', 'a', 'b', 'c', 'd', 'e', 'f')
    e_tup = (['s',6,'a'],
             ['s', 5, 'b'],
             ['s', 5, 'c'],
             ['a', -1, 'd'],
             ['b', -2, 'a'],
             ['b', 1, 'd'],
             ['c', -2, 'b'],
             ['c', -1, 'e'],
             ['d', 3, 'f'],
             ['e', 3, 'f'])
# test code for graphs that have negative loops.
#            ,['d', -9, 'b'])

    # generate the graph
    adj_matrix  = make_graph(num_v, num_e, v_tup, e_tup)

    # a dictionary to store the shortest path from s to any point
    # initialized to the current edge set we have
    shortest_path = [['0'] for _ in range (num_v)]
    for i in range(len(e_tup)):
        if e_tup[i][0] == 0: # if 's' is the starting V of an edge
            shortest_path[e_tup[i][2]].append(str(e_tup[i][2]))

    # a list to hold the current shortest path
    # initialized to current edge (first row of the adj_matrix)
    shortest_path_matrix = adj_matrix[0]

    # a variable to hold the shortest_path_matrix in the previous iteration
    # to detect negative loop
    previous_path_matrix = None
    has_neg_loop = False


    # relax evey edge
    for j in range(len(v_tup)):
        # store the previous iteration result in the second last iteration
        if j == (len(v_tup) - 1):
            previous_path_matrix = list(shortest_path_matrix)

        for i in range(len(e_tup)):
           relaxation(shortest_path, shortest_path_matrix, adj_matrix, e_tup[i])

    # determine if there's at least one negative loop
    if previous_path_matrix != shortest_path_matrix:
        has_neg_loop = True

    # a dictionary to convert index back to label
    num_to_label = {str(index): label for index, label in enumerate(v_tup)}

    print_shortest_path_matrix(shortest_path_matrix, num_to_label)
    print_shortest_path(shortest_path, num_to_label, v_tup)

    print('--------Negative Cycle?--------')
    print(f'This graph has{' no ' if has_neg_loop == False else ' at least one '}negative cycle')

