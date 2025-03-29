import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from tqdm import tqdm

from strategies import Move, strategies
from simulate import Winner, simulate_many


def tournament(
    strategy_names: list[str],
    num_games_per_pairing: int
) -> pd.DataFrame:
    """Run a tournament between all strategies."""
    results = pd.DataFrame(index=strategy_names,
                           columns=strategy_names,
                           dtype=float)

    progress_bar = tqdm(total = len(strategy_names)**2)
    for p1_strategy in strategy_names:
        for p2_strategy in strategy_names:
            progress_bar.update()
            result = simulate_many(
                strategies[p1_strategy],
                strategies[p2_strategy],
                num_games_per_pairing
            )
            p1_win_percentage = \
                result[Winner.PLAYER_1] / num_games_per_pairing * 100
            results.at[p1_strategy, p2_strategy] = p1_win_percentage

    results.index.name = "Player 1 Strategy"
    results.columns.name = "Player 2 Strategy"

    return results

if __name__ == "__main__":
    strategy_names = list(strategies.keys())
    n = 1000
    results = tournament(strategy_names, n)
    # results.to_csv("tournament_results.csv")

    plt.figure(figsize=(10, 8))
    plt.title("Tournament Results")
    ax = sns.heatmap(
        results,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        cbar=True,
        center=50,
        cbar_kws={'label': 'Win Percentage'},
        xticklabels=results.columns,
        yticklabels=results.index
    )
    ax.set(xlabel="player 2 strategy", ylabel="player 1 strategy")
    plt.show()
