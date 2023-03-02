import pandas as pd
scores = [
    [1, [1, 2, 3]],
    [2, [4, 5, 6]],
    [3, [7, 8, 9]]
]


def calculate_cumulative_scores(values):
    vals = [i[1] for i in scores]
    rounds = [i[0] for i in scores]

    df = pd.DataFrame(vals)
    cumulative_vals = df.cumsum().values.tolist()

    cumulative_scores = list(zip(rounds, cumulative_vals))

    return cumulative_scores
