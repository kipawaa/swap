# Theoretical Understanding via Density Matrices
(warning: density matrices typically refer to a form of state representation in quantum mechanics.
The use here is similar, so I stole the name)

there are 25 active game states with 10 end states (i.e. where a player has won). 
The final state is unreachable, and represents when both players have won, but we can ignore this caveat and represent the game with 6x6 matrix.
The columns represent the number of our own tiles that we control
The rows represent the number of our opponents tiles that we control
For example, if we're the starting player then the starting position is given by

```
initial_state = np.zeros((6,6))
initial_state[0, -1] = 1
```

$$
\begin{bmatrix}
0 & 0 & 0 & 0 & 0 & 1\\
0 & 0 & 0 & 0 & 0 & 0\\
0 & 0 & 0 & 0 & 0 & 0\\
0 & 0 & 0 & 0 & 0 & 0\\
0 & 0 & 0 & 0 & 0 & 0\\
0 & 0 & 0 & 0 & 0 & 0
\end{bmatrix}
$$

We can proceed to the next position by changing the entries.
We can do even better by using this as a "density matrix" (see warning below the title), representing the probabilities of a given state after $n$ turns.

there's a 1/2 probability that Alice fails the coin flip
```
second_state = 1/2 * initial_state
```

and a 1/2 probability that she succeeds
```
second_state[0, -2] = 1/2
```

$$
\begin{bmatrix}
0 & 0 & 0 & 0 & 0.5 & 0.5\\
0 & 0 & 0 & 0 & 0 & 0\\
0 & 0 & 0 & 0 & 0 & 0\\
0 & 0 & 0 & 0 & 0 & 0\\
0 & 0 & 0 & 0 & 0 & 0\\
0 & 0 & 0 & 0 & 0 & 0
\end{bmatrix}
$$

we can't continue deterministically from here because we don't know if our opponent will choose our tile or theirs.
This can be computed (to some extent) with symbolic manipulation (see theory.pdf).
Instead, lets do some analysis assuming two truly random agents.

On our turn:
- choosing our tile corresponds to moving left
- choosing our opponents tile corresponds to moving up

each of these has a 1/2 probability of being chosen, and a 1/2 probability of
success (i.e. winning the coin flip).
On failure, we stay in the same place.

On our opponents turn:
- choosing our tile corresponds to moving right
- choosing their tile corresponds to moving down

similar probabilities apply to our turn.

If we reach any cell $(r, 0)$ then we win, and if we reach any cell $(6, c)$ then we lose.

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

Notice that the winning states are accumulating probabilities here, so that after $n$ iterations the winning states represent the probability of reaching that state in $n$ turns *or less*.

This idea can be extended to any set of strategies by us or our opponent by altering the the probabilities or the way in which we update the cells.
