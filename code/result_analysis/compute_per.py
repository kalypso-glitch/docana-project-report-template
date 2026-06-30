#import pandas as pd
#results\mapped_reddit_posts_INCOMPLETE.csv
#results = pd.read_csv('C:\\git\\Studium\\Document_Analysis\\docana-project-report-template\\results\\mapped_reddit_posts_INCOMPLETE.csv')

import pandas as pd
import numpy as np
import os


# ---------------------------------------------------------
# Outlier-Filter (IQR-Methode)
# ---------------------------------------------------------
def remove_outliers(series: pd.Series) -> pd.Series:
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return series[(series >= lower) & (series <= upper)]


# ---------------------------------------------------------
# Aggregation pro Subreddit
# ---------------------------------------------------------
def agg_subreddit(df: pd.DataFrame) -> pd.DataFrame:
    groups = df.groupby("subreddit")["readability_index"]

    result = pd.DataFrame({
        "subreddit": groups.mean().index,
        "avg": groups.mean().values,
        "p90": groups.quantile(0.90).values,
        "p10": groups.quantile(0.10).values,
        "count_posts": groups.count().values,
    })

    result["avg_wo_outliers"] = (
        df.groupby("subreddit")["readability_index"]
          .apply(lambda s: remove_outliers(s).mean())
          .values
    )

    return result


# ---------------------------------------------------------
# Aggregation pro User
# ---------------------------------------------------------
def agg_user(df: pd.DataFrame) -> pd.DataFrame:
    groups = df.groupby("author")["readability_index"]

    result = pd.DataFrame({
        "author": groups.mean().index,
        "avg": groups.mean().values,
        "p90": groups.quantile(0.90).values,
        "p10": groups.quantile(0.10).values,
        "count_posts": groups.count().values,
    })

    result["avg_wo_outliers"] = (
        df.groupby("author")["readability_index"]
          .apply(lambda s: remove_outliers(s).mean())
          .values
    )

    return result


# ---------------------------------------------------------
# User–Subreddit Similarity
# ---------------------------------------------------------
def compute_user_sub_similarity(df, user_stats, sub_stats):
    df_user = df.merge(
        user_stats[["author", "avg"]].rename(columns={"avg": "user_avg"}),
        on="author"
    )

    df_user = df_user.merge(
        sub_stats[["subreddit", "avg"]].rename(columns={"avg": "sub_avg"}),
        on="subreddit"
    )

    df_user["diff"] = (df_user["user_avg"] - df_user["sub_avg"]).abs()
    df_user["user_minus_sub"] = df_user["user_avg"] - df_user["sub_avg"]

    return df_user


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------
def main():
    # relativer Pfad zur CSV-Datei
    base_path = os.path.join(os.path.dirname(__file__), "../../results/")
    file_path = os.path.join(os.path.dirname(__file__), "../../results/mapped_reddit_posts.csv")
    # CSV laden
    df = pd.read_csv(file_path)

    # Subreddit-Stats
    sub_stats = agg_subreddit(df)
    subreddit_stats_path = os.path.join(base_path, "subreddit_stats.csv")
    sub_stats.to_csv(subreddit_stats_path, index=False)

    # User-Stats
    user_stats = agg_user(df)
    user_stats_path = os.path.join(base_path, "user_stats.csv")
    user_stats.to_csv(user_stats_path, index=False)

    # User–Subreddit Vergleich
    similarity = compute_user_sub_similarity(df, user_stats, sub_stats)
    user_sub_similarity_path = os.path.join(base_path, "user_sub_similarity.csv")
    similarity.to_csv(user_sub_similarity_path, index=False)

    # Globale Werte
    global_avg = df["readability_index"].mean()
    global_p90 = df["readability_index"].quantile(0.90)
    global_p10 = df["readability_index"].quantile(0.10)

    print("Global Average:", global_avg)
    print("Global 90th Percentile:", global_p90)
    print("Global 10th Percentile:", global_p10)
    print("Done.")


if __name__ == "__main__":
    main()
