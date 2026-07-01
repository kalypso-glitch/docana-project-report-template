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

    result["avg_capped_25"] = (
        df.groupby("subreddit")["readability_index"]
        .apply(lambda s: s[s <= 25].mean())
        .values
    )

    #result["avg_capped_25"] = result["avg"].clip(upper=25)


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

    
    result["avg_capped_25"] = (
    df.groupby("author")["readability_index"]
      .apply(lambda s: s[s <= 25].mean())
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
def main(update_sub=False, update_user=True, update_similarity=False):
    base_path = os.path.join(os.path.dirname(__file__), "../../results/")
    file_path = os.path.join(base_path, "mapped_reddit_posts.csv")

    df = pd.read_csv(file_path, engine="pyarrow")

    # ---------------------------------------------------------
    # Subreddit-Stats
    # ---------------------------------------------------------
    if update_sub:
        sub_stats = agg_subreddit(df)
        #sub_stats["avg_capped_25"] = sub_stats["avg"].clip(upper=25)

        sub_stats_path = os.path.join(base_path, "subreddit_stats.csv")
        sub_stats.to_csv(sub_stats_path, index=False)
        print("Updated: subreddit_stats.csv")

    # ---------------------------------------------------------
    # User-Stats
    # ---------------------------------------------------------
    if update_user:
        user_stats = agg_user(df)
        #user_stats["avg_capped_25"] = user_stats["avg"].clip(upper=25)

        user_stats_path = os.path.join(base_path, "user_stats.csv")
        user_stats.to_csv(user_stats_path, index=False)
        print("Updated: user_stats.csv")

    # ---------------------------------------------------------
    # Similarity (braucht beide Stats)
    # ---------------------------------------------------------
    if update_similarity:
        # Falls nicht bereits oben berechnet → neu laden
        if not update_user:
            user_stats = pd.read_csv(os.path.join(base_path, "user_stats.csv"))
        if not update_sub:
            sub_stats = pd.read_csv(os.path.join(base_path, "subreddit_stats.csv"))

        similarity = compute_user_sub_similarity(df, user_stats, sub_stats)
        similarity_path = os.path.join(base_path, "user_sub_similarity.csv")
        similarity.to_csv(similarity_path, index=False)
        print("Updated: user_sub_similarity.csv")

    print("Done.")



if __name__ == "__main__":
    main()
