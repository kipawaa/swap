from copy import deepcopy
from enum import Enum
from random import randint, random
from fractions import Fraction

from strategies import Move, StrategyFunction

class Winner(Enum):
    PLAYER_1 = 0
    PLAYER_2 = 1

def simulate(p1_strategy: StrategyFunction, p2_strategy: StrategyFunction):
    """Simulate a game between two players using their strategies."""
    p1 = [5, 0]  # Player 1: [ours, theirs]
    p2 = [5, 0]  # Player 2: [ours, theirs]

    turn = 0

    while True:
        move_success = randint(0, 1)

        if move_success:
            if turn % 2 == 0:
                move = p1_strategy(*p1)
                assert move.mine >= 0 and move.theirs >= 0
                assert move.mine + move.theirs == 1
                prob = random()
                if prob < move.mine:
                    p1[0] -= 1
                    p2[1] += 1
                else:
                    assert p1[1] > 0
                    p1[1] -= 1
                    p2[0] += 1
            else:
                move = p2_strategy(*p2)
                assert move.mine >= 0 and move.theirs >= 0
                assert move.mine + move.theirs == 1
                prob = random()
                if prob < move.mine:
                    p2[0] -= 1
                    p1[1] += 1
                else:
                    assert p2[1] > 0
                    p2[1] -= 1
                    p1[0] += 1
        
        if p1[0] == 0:
            return Winner.PLAYER_1
        elif p2[0] == 0:
            return Winner.PLAYER_2
        
        turn += 1

def simulate_many(
    p1_strategy: StrategyFunction,
    p2_strategy: StrategyFunction,
    num_games: int
) -> dict[Winner, int]:
    """Simulate multiple games and return the results."""
    results = {Winner.PLAYER_1: 0, Winner.PLAYER_2: 0}

    for _ in range(num_games):
        winner = simulate(p1_strategy, p2_strategy)
        results[winner] += 1

    return results

def solve_system_exact(A, rhs):
    """Solve a system of equations using exact arithmetic."""
    n = len(A)
    
    # Make deep copies to avoid modifying the original input
    A = deepcopy(A)
    rhs = deepcopy(rhs)

    # Forward Elimination: Convert A to upper triangular form
    for i in range(n):
        # Pivoting: If diagonal element is zero, swap with a row below
        if A[i][i] == 0:
            for j in range(i + 1, n):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    rhs[i], rhs[j] = rhs[j], rhs[i]
                    break
            else:
                raise ValueError("Singular matrix encountered! Cannot solve.")
        
        # Normalize pivot row
        pivot = A[i][i]
        for k in range(n):
            A[i][k] /= pivot
        rhs[i] /= pivot

        # Eliminate entries below the pivot
        for j in range(i + 1, n):
            factor = A[j][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            rhs[j] -= factor * rhs[i]

    # Back Substitution: Solve for solution vector x
    x = [Fraction(0) for _ in range(n)]
    for i in reversed(range(n)):
        x[i] = rhs[i]
        for j in range(i + 1, n):
            x[i] -= A[i][j] * x[j]

    return x

def solve_exact(p1_strategy: StrategyFunction, p2_strategy: StrategyFunction):
    """Solve a matchup outcome exactly using a linear system solver
    with exact arithmetic."""
    all_states = [
        (p1_ours, p1_theirs, turn)
        for p1_ours in range(6)
        for p1_theirs in range(6)
        for turn in range(2)
    ]
    state_index = { s: i for i, s in enumerate(all_states) }
    state_is_terminal = lambda s: s[0] == 0 or s[1] == 5
    state_terminal_value = lambda s: Fraction(1, 1) if s[0] == 0 else (Fraction(0, 1) if s[1] == 5 else None)

    state_matrix = [
        [Fraction(0, 1)] * len(all_states)
        for _ in range(len(all_states))
    ]
    rhs = [Fraction(0, 1)] * len(all_states)

    # Populate the A matrix and rhs vector
    for i, s in enumerate(all_states):
        state_matrix[i][i] = Fraction(1, 1)
        if state_is_terminal(s):
            rhs[i] = state_terminal_value(s)
            continue
        p1_ours, p1_theirs, turn = s
        success_rate = Fraction(1, 2)
        state_matrix[i][state_index[(p1_ours, p1_theirs, (1 - turn))]] -= (Fraction(1, 1) - success_rate)
        if turn == 0:
            move = p1_strategy(p1_ours, p1_theirs)
            assert move.mine >= 0 and move.theirs >= 0
            assert move.mine + move.theirs == 1
            if move.mine > 0:
                state_matrix[i][state_index[(p1_ours - 1, p1_theirs, 1)]] -= success_rate * move.mine
            if move.theirs > 0:
                state_matrix[i][state_index[(p1_ours, p1_theirs - 1, 1)]] -= success_rate * move.theirs
        else:
            p2_ours = 5 - p1_theirs
            p2_theirs = 5 - p1_ours
            move = p2_strategy(p2_ours, p2_theirs)
            assert move.mine >= 0 and move.theirs >= 0
            assert move.mine + move.theirs == 1
            if move.mine > 0:
                state_matrix[i][state_index[(p1_ours, p1_theirs + 1, 0)]] -= success_rate * move.mine
            if move.theirs > 0:
                state_matrix[i][state_index[(p1_ours + 1, p1_theirs, 0)]] -= success_rate * move.theirs
    
    # Solve the system of equations using Gaussian elimination
    solution = solve_system_exact(state_matrix, rhs)
    p1_win_probability = solution[state_index[(5, 0, 0)]]
    return p1_win_probability
