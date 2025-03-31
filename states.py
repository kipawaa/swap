import numpy as np

initial_state = np.zeros((6,6))
initial_state[0, -1] = 1
print("initial state:")
print(initial_state)

second_state = 1/2 * initial_state
second_state[0, 4] = 1/2
print("after first move:")
print(second_state)

def our_turn(state):
    # there's a 50% chance of losing the coin flip, i.e. no change
    newstate = state / 2

    # there's a 1/4 chance of moving to the left if we have a tile of each type
    newstate[1:-1, :-1] += state[1:-1, 1:] / 4
    newstate[0, :-1] += state[0, 1:] / 2 # but a 1/2 chance if we only have our own tiles

    # there's a 1/4 chance of moving up
    newstate[:-2, 1:] += state[1:-1, 1:] / 4
    return newstate

def opp_turn(state):
    # there's a 50% chance of losing the coin flip, i.e. no change
    newstate = state / 2

    # there's a 1/4 chance of moving down if they have a tile of each type
    newstate[1:, 1:-1] += state[:-1, 1:-1] / 4
    newstate[1:, -1] += state[:-1, -1] / 2 # but a 1/2 chance if they only have their own tiles

    # there's a 1/4 chance of moving right
    newstate[:-1, 2:] += state[:-1, 1:-1] / 4
    return newstate

num_turns = 10
state = initial_state

for t in range(num_turns):
    if t % 2 == 0:
        state = our_turn(state)
    else:
        state = opp_turn(state)

np.set_printoptions(formatter={'float': lambda x: f"{x:0.3f}"})
print(f"after {num_turns} turns:")
print(state)
