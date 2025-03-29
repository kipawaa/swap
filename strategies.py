from enum import Enum
from typing import Callable

from random import randint

class Move(Enum):
    MINE = 0
    THEIRS = 1

    def __str__(self):
        return move_to_str[self]

move_to_str = {
    Move.MINE: "mine",
    Move.THEIRS: "theirs"
}

StrategyFunction = Callable[[int, int, list[Move]], Move]

strategies: dict[str, StrategyFunction] = {}

def register_strategy(func: StrategyFunction) -> StrategyFunction:
    strategies[func.__name__] = func
    return func

##############
# Strategies #
##############

# Deterministic strategies

@register_strategy
def max_greed(*args) -> Move:
    """Always choose mine."""
    return Move.MINE

@register_strategy
def medium_greed(ours: int, theirs: int, *args) -> Move:
    """Choose ours unless we are about to lose."""
    if theirs == 4:
        return Move.THEIRS
    return Move.MINE

@register_strategy
def medium_greedier(ours: int, theirs: int, *args) -> Move:
    """Choose ours unless we are about to lose and not about to win."""
    if theirs == 4 and ours != 1:
        return Move.THEIRS
    return Move.MINE

@register_strategy
def low_greed(ours: int, theirs: int, *args) -> Move:
    """Choose ours unless we are 2 or less away from losing."""
    if theirs >= 3:
        return Move.THEIRS
    return Move.MINE

@register_strategy
def low_greedier(ours: int, theirs: int, *args) -> Move:
    """Choose ours unless we are 2 or less away from losing 
    and not 2 or less away from winning."""
    if theirs >= 3 and ours > 2:
        return Move.THEIRS
    return Move.MINE

@register_strategy
def defensive(ours: int, theirs: int, *args) -> Move:
    """Choose theirs whenever possible."""
    if theirs > 0:
        return Move.THEIRS
    return Move.MINE

@register_strategy
def balanced(ours: int, theirs: int, *args) -> Move:
    """Choose ours when closer to winning than they are."""
    needed_to_win = ours
    needed_to_lose = 5 - theirs
    if needed_to_win <= needed_to_lose:
        return Move.MINE
    return Move.THEIRS

# Non-deterministic strategies

@register_strategy
def random(ours: int, theirs: int, *args) -> Move:
    """Randomly choose to get rid of mine or theirs."""
    if theirs != 0:
        return Move(randint(0, 1))
    return Move.MINE

@register_strategy
def random_with_attack(ours: int, theirs: int, *args) -> Move:
    """Randomly choose to get rid of mine or theirs, but choose ours
    when we are one shot away from winning."""
    if theirs != 0:
        if ours != 1 and randint(0, 1):
            return Move.THEIRS
    return Move.MINE

@register_strategy
def random_with_defend(ours: int, theirs: int, *args) -> Move:
    """Randomly choose to get rid of mine or theirs, but choose theirs
    when we are one shot away from losing."""
    if theirs != 0:
        if theirs == 4 or randint(0, 1):
            return Move.THEIRS
    return Move.MINE

@register_strategy
def random_with_defend_and_attack(ours: int, theirs: int, *args) -> Move:
    """Randomly choose to get rid of mine or theirs, but choose ours"
    when we are one shot away from winning and choose theirs when
    we are one shot away from losing."""
    if theirs != 0 and ours != 1:
        if theirs == 4 or randint(0, 1):
            return Move.THEIRS
    return Move.MINE
