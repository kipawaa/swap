import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from tqdm import tqdm

from strategies import Move, strategies, format_strategy_name
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

    score_p1 = results.mean(axis=1)
    score_p2 = 100 - results.mean(axis=0)
    avg_score = (score_p1 + score_p2) / 2
    results["AverageWinRate"] = avg_score
    sorted_index = avg_score.sort_values(ascending=False).index
    results = results.loc[sorted_index, sorted_index]

    return results

if __name__ == "__main__":
    strategy_names = list(strategies.keys())
    n = 10000
    results = tournament(strategy_names, n)
    results.to_csv("results.csv")

    plt.figure(figsize=(15, 13))
    plt.title("Tournament Results")
    ax = sns.heatmap(
        results,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        cbar=True,
        center=50,
        cbar_kws={'label': 'Win Percentage'},
        xticklabels=list(map(format_strategy_name, results.columns)),
        yticklabels=list(map(format_strategy_name, results.index))
    )
    ax.set(xlabel="Player 2 Strategy", ylabel="Player 1 Strategy")
    ax.figure.tight_layout()
    plt.show()
