from enum import Enum
from random import randint, random

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
