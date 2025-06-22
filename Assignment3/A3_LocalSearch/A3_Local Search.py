import math
import random

import pandas as pd
import matplotlib.pyplot as plt
from PIL.ImageChops import difference
from matplotlib.animation import FuncAnimation

df = pd.read_csv("Data.csv")

# The neighborhood for any point Si i Î {2,..99} is defined as {Si-1 and Si+1}

# A figure with axes
fig, ax = plt.subplots()
# the axes limits xmin, x max, y min, y max
ax.axis([0,100,0,10000])
# create a point in the axes, we are plotting the data from CSV file "Data.csv" . 
# Assume that, there are 100 possible sates Si where i = (1...100) 
# Each state (except state 1 and 100) have exactly 2 neighbours. Si has neighbors Si-1 and Si+1
# Data.csv directly provides the reward/utility of every state (1 to 100). Column named "State" corresponds to state number and its respective row " Reward" corresponds to utility of the state.
ax.plot(df['State'],df['Reward'])
# An animated point used to show the current state on the plot.
point, = ax.plot(0,1, marker="o")


# we will randomly use a state as the initial state. Indexing starts from 0, therefore, we are ommiting that first and last row
start_state = 57 #random.randint(1,98)
#Initially current state = start state.
cur_state=start_state

#Temperature = 4000, use this for Section 2, Q2
T = 4000

#A simple hillclimbing method, without sideway moves,  is implemented as an example
def HillClimbNoSideways(time):
    global cur_state #access the curstate as global variable

    #checks neighbors and move only if utility is strictly greater than current state.
    #The point is returned to the animating function which displays it on the plot.
    #Use this code an as example to complete the other two functions.
    if(df["Reward"][cur_state+1] >df["Reward"][cur_state]):
        cur_state=min(cur_state+1,98)
        point.set_data([cur_state], [df['Reward'][cur_state]])
        return point
    elif ( df["Reward"][cur_state - 1]>df["Reward"][cur_state] ):
        cur_state = max(cur_state - 1,1)
        point.set_data([cur_state], [df['Reward'][cur_state]])
        return point
    return point

""" DO NOT MAKE MODIFICATIONS ABOVE THIS LINE"""
#______________________________________________

last_state = 'left'
last_sideway = False
def HillClimbWithSideways(time):
    global cur_state
    global last_state
    global last_sideway
    # Complete the code in this function to implement a better hillclimbing
    # method which allows sideways moves with 0.5 probability

    # see if sideway is encountered, otherwise just use the regular hill climb w/o sideways
    left_neighbor = df["Reward"][cur_state] == df["Reward"][cur_state - 1]
    right_neighbor = df["Reward"][cur_state] == df["Reward"][cur_state + 1]
    probability = random.randint(0,100) / 100

    print(f'L: {left_neighbor}, R: {right_neighbor},'
          f' Prob: {probability}, Post: {cur_state}',
          f' Last: {last_state}')
    if (left_neighbor and probability >= 0.5 and
            (not last_sideway or last_state != 'right')):
        cur_state = max(cur_state - 1,1)
        point.set_data([cur_state + 1 ], [df['Reward'][cur_state]])
        last_state = 'left'
        last_sideway = True
        return point

    elif (right_neighbor and probability >= 0.5 and
          (not last_sideway or last_state != 'left') ):
        cur_state = min(cur_state + 1,98)
        point.set_data([cur_state + 1 ], [df['Reward'][cur_state]])
        last_state = 'right'
        last_sideway = True
        return point
    else:
        old_data = point.get_xydata()
        new_point =  HillClimbNoSideways(time)
        new_data = new_point.get_xydata()
        print(f'Old: {old_data}, New: {new_data}')
        last_sideway = False
        if math.trunc(old_data[0][0]) < math.trunc(new_data[0][0]): # meaning new move will be right
            last_state = 'right'
        elif math.trunc(old_data[0][0]) > math.trunc(new_data[0][0]):
            last_state = 'left'
        return new_point


iteration_count = 0
def SimulatedAnnealing(time):
    print()

    global cur_state
    global iteration_count
    print(f'iteration: {iteration_count}')
    global T
    # Complete the code in this function to implement a Simulated annealing method
    # which allows all upward moves and
    # which allows downward moves with probability p = e^(delta/T)
    # delta stands for the difference in state utility.
    # Use a linearly decreasing T, that is, T=T-1 every iteration.
    # The Algorithm must randomly select a neighbor with probability 0.5,
    # then allow downward moves with probability p

    next_step = random.randint(0,1) # generates a random int between 0 and 1
    # if we rolled 1, check right
    # if we rolled 0, check left
    if not next_step:
        next_step = -1

    # cur_state is index
    # when setting the data point: index
    # when accessing the df: index
    # in df state number = index + 1
    # ex. 51,2800 is index 50

    if cur_state <= 2:
        cur_state = 2
    elif cur_state >= 98:
        cur_state = 98
    print(f'current state (index): {cur_state}')
    print(f'Current state in df acc by index: {df["State"][cur_state]}')
    print(f'Current reward in df acc by index:, {df["Reward"][cur_state]}')
    point.set_data([cur_state + 1], [df['Reward'][cur_state]])
    print(f'Current data: {point.get_xydata()}, Rolled: {next_step}, '
          f'Dir: {"right" if next_step == 1 else "left"}')


    next_state = cur_state + next_step
    difference = (df["Reward"][next_state] - df["Reward"][cur_state])

    print(f'Next state (index): {next_state}')
    print(f'Next state in df acc by index: {df["State"][next_state]}')
    print(f'Next reward in df acc by index:, {df["Reward"][next_state]}')

    # if the next_state reward is larger
    if difference > 0: # meaning the next state is a better choice or an equal choice
        point.set_data([next_state + 1], [df['Reward'][next_state]])
        print(f'new data: {point.get_xydata()}')

    elif difference == 0:
        iteration_count += 1 #increment the iteration count
        cur_state = next_state #update the current state
        print()
        return HillClimbWithSideways(time)
    else: # meaning the next state will be a downhill

        downward_p = math.e ** (difference/ (T - iteration_count))
        print(f'DH Prob: {downward_p}')
        decision =  random.random()
        if decision <= downward_p: # we take the downward path
            print(f'Dec: {decision}, Decision: DH')
            point.set_data([next_state + 1], [df['Reward'][next_state]])
        else:
            print(f'Dec: {decision}, Decision: stay')
            point.set_data([cur_state + 1], [df['Reward'][cur_state]])
            iteration_count += 1 #increment the iteration count
            print()
            return point

    iteration_count += 1 #increment the iteration count
    cur_state = next_state #update the current state
    print()
    return point

""" DO NOT MAKE MODIFICATIONS BELOW THIS LINE, Except for the second parameter in FuncAnimation call"""
#______________________________________________

# This  animation with 50ms interval, which is repeated,
# The second parameter, the function name, is the function that is called
# repeatedly for "frames" (sixth parameter) number of times.
ani = FuncAnimation(fig,SimulatedAnnealing, interval=50, blit=False, repeat=False, frames=5000)
plt.show()
