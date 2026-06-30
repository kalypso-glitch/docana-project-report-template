import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import statsmodels.api as sm


output_dir = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(output_dir, exist_ok=True)


df = pd.read_csv(
    r"data\user_stats.csv")


# Remove missing values
df = df.dropna(subset=["count_posts", "avg_capped_25"])

#removing the two highest posting users (possible bots)
df = df.sort_values(by="count_posts", ascending=False)
df = df.iloc[2:].copy()



# Independent variable
df["log_posts"] = np.log1p(df["count_posts"])

#dependent variable
complexity = df["avg_capped_25"]

#descriptive statistics
print(df[["count_posts", "log_posts", "avg_capped_25"]].describe())


#linear regression
X = sm.add_constant(df["log_posts"])
model = sm.OLS(complexity, X).fit()

print(model.summary())

# Scatter plot with regression line

plt.figure(figsize=(8, 6))

plt.scatter(
    df["log_posts"],
    complexity,
    alpha=0.02,
    s=5
)

predicted = model.predict(X)

plt.plot(
    df["log_posts"],
    predicted,
    color="red",
    linewidth=2
)

plt.xlabel("Log(Number of Posts + 1)")
plt.ylabel("Average Gunning Fog Index (Capped at 25)")
plt.title("Linear Regression")

plt.tight_layout()

plt.savefig(
    os.path.join(output_dir, "linear_regression.png"),
    dpi=300
)

plt.close()

# Distribution of post counts

plt.figure(figsize=(8, 6))

plt.hist(
    df["count_posts"],
    bins=100
)

plt.xlabel("Number of Posts")
plt.ylabel("Number of Users")
plt.title("Distribution of User Post Counts")

plt.tight_layout()

plt.savefig(
    os.path.join(output_dir, "post_count_distribution.png"),
    dpi=300
)

plt.close()

# Distribution of complexity

plt.figure(figsize=(8, 6))

plt.hist(
    complexity,
    bins=50
)

plt.xlabel("Average Gunning Fog Index (Capped at 25)")
plt.ylabel("Number of Users")
plt.title("Distribution of Average Post Complexity")

plt.tight_layout()

plt.savefig(
    os.path.join(output_dir, "complexity_distribution.png"),
    dpi=300
)

plt.close()

#print("\nAnalysis completed successfully.")