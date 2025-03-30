import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import multiprocessing

from tqdm import tqdm

from strategies import Move, strategies, format_strategy_name
from simulate import Winner, simulate_many


def _simulate_matchup(args):
    p1_strategy, p2_strategy, num_games = args
    result = simulate_many(
        strategies[p1_strategy],
        strategies[p2_strategy],
        num_games
    )
    p1_win_percentage = result[Winner.PLAYER_1] / num_games * 100
    return p1_strategy, p2_strategy, p1_win_percentage


def tournament(
    strategy_names: list[str],
    num_games_per_pairing: int
) -> pd.DataFrame:
    """Run a tournament between all strategies."""
    tasks = [(p1, p2, num_games_per_pairing)
             for p1 in strategy_names
             for p2 in strategy_names]
    results = pd.DataFrame(index=strategy_names,
                           columns=strategy_names,
                           dtype=float)

    progress_bar = tqdm(total=len(tasks))
    num_processes = multiprocessing.cpu_count() - 1
    # num_processes = 1
    with multiprocessing.Pool(processes=num_processes) as pool:
        for p1, p2, p1_win_percentage in pool.imap_unordered(_simulate_matchup, tasks):
            results.at[p1, p2] = p1_win_percentage
            progress_bar.update()

    score_p1 = results.mean(axis=1)
    score_p2 = 100 - results.mean(axis=0)
    avg_score = (score_p1 + score_p2) / 2
    results["AverageWinRate"] = avg_score
    sorted_index = avg_score.sort_values(ascending=False).index
    results = results.loc[sorted_index, sorted_index]
    results["average_winrate"] = avg_score[sorted_index]
    results["winrate_as_player1"] = score_p1[sorted_index]
    results["winrate_as_player2"] = score_p2[sorted_index]

    return results

if __name__ == "__main__":
    strategy_names = list(strategies.keys())
    n = 100000
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
    ax.axvline(x=len(strategy_names), color='black', linewidth=3)
    ax.set(xlabel="Player 2 Strategy", ylabel="Player 1 Strategy")
    ax.figure.tight_layout()
    plt.show()
