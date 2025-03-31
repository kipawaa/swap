# Theoretical Understanding via Density Matrices
(warning: density matrices typically refer to a form of state representation in quantum mechanics.
The use here is similar, so I stole the name)

there are 25 game states
represent with 6x6 matrix (we can have 0-5 of each)
col = number of our own tiles
row = number of our opponents tiles
for example, the starting position from Alice's perspective is given by

```
initial_state = np.zeros((6,6))
initial_state[0, -1] = 1
print("initial state:")
print(initial_state)
```

we can proceed to the next position by changing the entries.
we can do even better by using this as a density matrix, representing
the probabilities of a given state

there's a 1/2 probability that Alice fails the coin flip
```
second_state = 1/2 * initial_state
```

and a 1/2 probability that she succeeds
```
second_state[0, 4] = 1/2
print("after first move:")
print(second_state)
```

we can't continue deterministically from here because we don't know if bob
will choose our tile or his
this can be computed (to some extent) with symbolic manipulation
(see theory.pdf)

instead, lets do some analysis assuming two truly random agents.
every non-zero cell of the matrix represents a state that the game could be
in.

on our turn:
  choosing our tile corresponds to moving left
  choosing our opponents tile corresponds to moving up
each of these has a 1/2 probability of being chosen, and a 1/2 probability of
success.
on failure, we stay in the same place

on our opponents turn:
  choosing our tile corresponds to moving right
  choosing their tile corresponds to moving down
similar probabilities apply

if we reach cell x, 0 then we win, and if we reach 6, y then we lose

so we can implement:
```
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
```

and we can now simulate any number of turns, then check the probabilities of
a given state after that many turns.

```
num_turns = 10
state = initial_state
for t in range(num_turns):
    if t % 2 == 0:
        state = our_turn(state)
    else:
        state = opp_turn(state)
```

np.set_printoptions(formatter={'float': lambda x: f"{x:0.3f}"})
print(f"after {num_turns} turns:")
print(state)

and this can be extended to any set of strategies by us or our opponent by 
altering the probabilities
