from datetime import datetime
import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

md_file = "General_Subreddits.md"

output_dir = "figures"

def save_fig_from_title():
    # Titel aus der aktuellen Figure holen
    title = plt.gca().get_title()

    if not title:
        raise ValueError("Der Plot hat keinen Titel – bitte plt.title() setzen!")

    # Titel in Dateinamen umwandeln
    safe_title = re.sub(r'[^a-zA-Z0-9_-]', '_', title)

    # Zeitstempel für Eindeutigkeit
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"{timestamp}_{safe_title}.png"
    filepath = os.path.join(output_dir, filename)

    plt.savefig(filepath, dpi=300, bbox_inches="tight")
    print(f"Saved: {filepath}")

# ---------------------------------------------------------
# 1. Daten laden
# ---------------------------------------------------------
df = pd.read_csv("results/subreddit_stats.csv")

# Filter: nur Subreddits mit >50 Posts
df_big = df[df["count_posts"] > 50].copy()

print(f"Count Subreddits >50 Posts: {len(df_big)}")

# ---------------------------------------------------------
# 2. Globale Statistik
# ---------------------------------------------------------
print("\n--- Globale Statistics ---")
print(df_big[["avg", "p90", "p10", "avg_wo_outliers"]].describe())

# ---------------------------------------------------------
# 3. Verteilungen
# ---------------------------------------------------------
plt.figure(figsize=(10,5))
sns.histplot(df_big["avg"], kde=True, bins=40)
plt.title("Distribution of the avg-Readability score")
plt.xlabel("avg")
plt.ylabel("Frequency")
plt.tight_layout()
#plt.show()
save_fig_from_title()
plt.close()
plt.figure(figsize=(10,5))
sns.histplot(df_big["p90"], kde=True, bins=40, color="orange")
plt.title("Distribution of p90 Readability")
plt.xlabel("p90")
plt.tight_layout()
#plt.show()
save_fig_from_title()
plt.close()
# ---------------------------------------------------------
# 4. Varianz & p90–p10 Spanne
# ---------------------------------------------------------
df_big["span"] = df_big["p90"] - df_big["p10"]

plt.figure(figsize=(10,5))
sns.histplot(df_big["span"], kde=True, bins=40, color="green")
plt.title("Linguistic Range (p90 - p10)")
plt.xlabel("Range")
plt.tight_layout()
#plt.show()
save_fig_from_title()
plt.close()
print("\nSubreddits with the widest range:")
print(df_big.nlargest(10, "span")[["subreddit", "span"]])

# ---------------------------------------------------------
# 5. Clustering (K-Means)
# ---------------------------------------------------------
features = df_big[["avg", "p90", "p10", "span"]]

scaler = StandardScaler()
X = scaler.fit_transform(features)

kmeans = KMeans(n_clusters=4, random_state=42)
df_big["cluster"] = kmeans.fit_predict(X)

plt.figure(figsize=(10,6))
sns.scatterplot(
    data=df_big,
    x="avg",
    y="span",
    hue="cluster",
    palette="tab10"
)
plt.title("Clusters of subreddits by writing style")
plt.xlabel("avg")
plt.ylabel("span (p90 - p10)")
plt.tight_layout()
#plt.show()
save_fig_from_title()
plt.close()
# ---------------------------------------------------------
# 6. Regression: Schreibstil vs. Aktivität
# ---------------------------------------------------------
plt.figure(figsize=(10,6))
sns.regplot(
    data=df_big,
    x=np.log(df_big["count_posts"]),
    y="avg",
    scatter_kws={"alpha":0.3}
)
plt.title("Context: Activity vs. Writing Complexity")
plt.xlabel("log(count_posts)")
plt.ylabel("avg")
plt.tight_layout()
#plt.show()
save_fig_from_title()
plt.close()
corr = np.corrcoef(np.log(df_big["count_posts"]), df_big["avg"])[0,1]
print(f"\nCorrelation log(count_posts) vs avg: {corr:.3f}")

# ---------------------------------------------------------
# 7. Outlier-Analyse
# ---------------------------------------------------------
df_big["outlier_diff"] = df_big["avg"] - df_big["avg_wo_outliers"]

plt.figure(figsize=(10,5))
sns.histplot(df_big["outlier_diff"], kde=True, bins=40, color="red")
plt.title("Impact of Outliers (avg - avg_wo_outliers)")
plt.xlabel("Difference")
plt.tight_layout()
#plt.show()
save_fig_from_title()
plt.close()
print("\nSubreddits with the strongest outlier effect:")
print(df_big.nlargest(10, "outlier_diff")[["subreddit", "outlier_diff"]])

# ---------------------------------------------------------
# Markdown: Anzahl Subreddits
# ---------------------------------------------------------
with open(md_file, "a", encoding="utf-8") as f:
    f.write("## Number of subreddits with more than 50 posts\n\n")
    f.write(f"**{len(df_big)} Subreddits** meet the threshold of >50 posts.\n\n")

# ---------------------------------------------------------
# Markdown: Globale Statistik
# ---------------------------------------------------------
stats = df_big[["avg", "p90", "p10", "avg_wo_outliers"]].describe()

# DataFrame → Markdown-Tabelle
stats_md = stats.to_markdown()

with open(md_file, "a", encoding="utf-8") as f:
    f.write("## Globale Statistics\n\n")
    f.write(stats_md + "\n\n")

# ---------------------------------------------------------
# Markdown: Subreddits mit größter Spannweite
# ---------------------------------------------------------
top_span = df_big.nlargest(10, "span")[["subreddit", "span"]]

span_md = "| Subreddit | Range (p90 - p10) |\n|---|---|\n"
for _, row in top_span.iterrows():
    span_md += f"| {row['subreddit']} | {row['span']:.6f} |\n"

with open(md_file, "a", encoding="utf-8") as f:
    f.write("## Subreddits with the widest range\n\n")
    f.write(span_md + "\n")

# ---------------------------------------------------------
# Markdown: Korrelation
# ---------------------------------------------------------
with open(md_file, "a", encoding="utf-8") as f:
    f.write("## Correlation Between Activity and Writing Complexity\n\n")
    f.write(f"The correlation between **log(count_posts)** and **avg** is: **{corr:.3f}**.\n\n")

# ---------------------------------------------------------
# Markdown: Subreddits mit stärkstem Outlier-Effekt
# ---------------------------------------------------------
top_outliers = df_big.nlargest(10, "outlier_diff")[["subreddit", "outlier_diff"]]

outlier_md = "| Subreddit | Outlier-Difference |\n|---|---|\n"
for _, row in top_outliers.iterrows():
    outlier_md += f"| {row['subreddit']} | {row['outlier_diff']:.6f} |\n"

with open(md_file, "a", encoding="utf-8") as f:
    f.write("## Subreddits with the Strongest Outlier Effect\n\n")
    f.write(outlier_md + "\n")
