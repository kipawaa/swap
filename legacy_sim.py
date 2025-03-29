import pandas as pd
from tqdm import tqdm
from random import randint

strats = ("defensive", "balanced", "max_greed", "greed", "random", "random+")

def shoot(selected, p1, p2):
    # if shot is successful
    if randint(0, 1):
        if selected="own":
            p1[0] -= 1
            p2[1] +=1
        elif selected="other":
            p1[1] -= 1
            p2[0] += 1

def strat(player, opponent, strategy=None):
    match strategy:
        case "defensive":
            # get rid of all opponents before trying to win
            if player[1] != 0:
                shoot("other", p1, p2)
            else:
                if randint(0, 1):
                    player[0] -= 1
                    opponent[1] += 1
        
        case "balanced":
            # its good i promise
            if player[0] > 5 - player[1]:
                if randint(0, 1):
                    player[1] -= 1
                    opponent[0] += 1
            else:
                if randint(0, 1):
                    player[0] -= 1
                    opponent[1] += 1

        case "max_greed":
            # always choose mine
            if randint(0, 1):
                player[0] -= 1
                opponent[1] += 1

        case "greed":
            # get rid of mine unless about to lose
            if player[1] == 4:
                if randint(0, 1):
                    player[1] -= 1
                    opponent[0] += 1
            else:
                if randint(0, 1):
                    player[0] -= 1

        case "random+":
            # random but choose theirs if we are about to lose (mix random + greed)
            if player[1] != 0:
                if player[1] == 4 or randint(0, 1):
                    if randint(0, 1):
                        player[1] -= 1
                        opponent[0] += 1
                else:
                    if randint(0, 1):
                        player[0] -= 1
                        opponent[1] += 1
            else:
                if randint(0, 1):
                    player[0] -= 1
                    opponent[1] += 1
               
        case "random":
            # randomly choose to get rid of mine or theirs
            if player[1] != 0:
                if randint(0, 1):
                    if randint(0, 1):
                        player[1] -= 1
                        opponent[0] += 1
                else:
                    if randint(0, 1):
                        player[0] -= 1
                        opponent[1] += 1
            else:
                if randint(0, 1):
                    player[0] -= 1
                    opponent[1] += 1

        case _:
            print("oof")
            raise TypeError


def has_won(player):
    return player[0] == 0

if __name__ == "__main__":
    n = 1000

    results = pd.DataFrame(index=strats, columns=strats)

    for p1_strat in tqdm(strats):
        for p2_strat in tqdm(strats):
            p1_wins = 0
            p2_wins = 0

            

            for i in tqdm(range(n)):
                p1 = [5, 0]
                p2 = [5, 0]

                turn = 0

                while not has_won(p1) and not has_won(p2):
                    if turn % 2 == 0:
                        strat(p1, p2, strategy=p1_strat)
                    else:
                        strat(p2, p1, strategy=p2_strat)
                    turn += 1

                if has_won(p1):
                    p1_wins += 1
                else:
                    p2_wins += 1

            results[p1_strat][p2_strat] = f"{p1_wins * 100 / n:.2f}"
    
    print(results)
