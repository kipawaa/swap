from enum import Enum
from typing import Callable

from random import randint

class Move:
    def __init__(self, mine: float, theirs: float):
        self.mine = mine
        self.theirs = theirs
    
    @staticmethod
    def MINE():
        return Move(1, 0)
    
    @staticmethod
    def THEIRS():
        return Move(0, 1)

StrategyFunction = Callable[[int, int], Move]

strategies: dict[str, StrategyFunction] = {}

def register_strategy(func: StrategyFunction) -> StrategyFunction:
    strategies[func.__name__] = func
    return func

def format_strategy_name(strategy_name: str) -> str:
    """Format the strategy name for display."""
    return strategy_name.replace("_", " ").title()

##############
# Strategies #
##############

# Deterministic strategies

@register_strategy
def max_greed(*args) -> Move:
    """Always choose mine."""
    return Move.MINE()

@register_strategy
def medium_greed(ours: int, theirs: int) -> Move:
    """Choose ours unless we are about to lose."""
    if theirs == 4:
        return Move.THEIRS()
    return Move.MINE()

@register_strategy
def medium_greedier(ours: int, theirs: int) -> Move:
    """Choose ours unless we are about to lose and not about to win."""
    if theirs == 4 and ours != 1:
        return Move.THEIRS()
    return Move.MINE()

@register_strategy
def low_greed(ours: int, theirs: int) -> Move:
    """Choose ours unless we are 2 or less away from losing."""
    if theirs >= 3:
        return Move.THEIRS()
    return Move.MINE()

@register_strategy
def low_greedier(ours: int, theirs: int) -> Move:
    """Choose ours unless we are 2 or less away from losing 
    and not 2 or less away from winning."""
    if theirs >= 3 and ours > 2:
        return Move.THEIRS()
    return Move.MINE()

# Developed using policy iteration to be optimal against
# low_greed strategy. As P1, should win 831818/1361367 (61.1%)
@register_strategy
def low_greed_beater(ours: int, theirs: int) -> Move:
    """Choose ours unless we are 2 or less away from losing 
    and not 2 or less away from winning and not about to win."""
    if ours == 4 and theirs >= 3:
        return Move.THEIRS()
    if ours == 5 and theirs >= 2:
        return Move.THEIRS()
    return Move.MINE()

@register_strategy
def defensive(ours: int, theirs: int) -> Move:
    """Choose theirs whenever possible."""
    if theirs > 0:
        return Move.THEIRS()
    return Move.MINE()

# Developed using policy iteration to be optimal against itself.
# As P1, should win 10/19 (52.6%)
@register_strategy
def game_theory_optimal(ours: int, theirs: int) -> Move:
    """Choose ours when closer to winning than they are."""
    needed_to_win = ours
    needed_to_lose = 5 - theirs
    if needed_to_win <= needed_to_lose:
        return Move.MINE()
    return Move.THEIRS()

# Non-deterministic strategies

@register_strategy
def random(ours: int, theirs: int) -> Move:
    """Randomly choose to get rid of mine or theirs."""
    if theirs != 0:
        return Move(0.5, 0.5)
    return Move.MINE()

@register_strategy
def random_with_attack(ours: int, theirs: int) -> Move:
    """Randomly choose to get rid of mine or theirs, but choose ours
    when we are one shot away from winning."""
    if theirs != 0:
        if ours != 1:
            return Move(0.5, 0.5)
    return Move.MINE()

@register_strategy
def random_with_defend(ours: int, theirs: int) -> Move:
    """Randomly choose to get rid of mine or theirs, but choose theirs
    when we are one shot away from losing."""
    if theirs != 0:
        if theirs == 4:
            return Move.THEIRS()
        return Move(0.5, 0.5)
    return Move.MINE()

@register_strategy
def random_with_defend_and_attack(ours: int, theirs: int) -> Move:
    """Randomly choose to get rid of mine or theirs, but choose ours"
    when we are one shot away from winning and choose theirs when
    we are one shot away from losing."""
    if theirs != 0 and ours != 1:
        if theirs == 4:
            return Move.THEIRS()
        return Move(0.5, 0.5)
    return Move.MINE()
