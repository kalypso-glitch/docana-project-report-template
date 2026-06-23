from code.sub_comparison.csv_reader import read_csv
import math

sub_data_path = "data/subreddit_stats.csv"
sub_data = read_csv(sub_data_path)

mapped_posts_path = "results/mapped_reddit_posts.csv"
mapped_posts_data = read_csv(mapped_posts_path)


def top_x_subreddits(x: int) -> list[dict]:
    sorted_data = sorted(sub_data, key=lambda row: int(row["count_posts"]), reverse=True)
    return sorted_data[:x]

def subs_with_posts_greater_than(x: int) -> list[dict]:
    return [row for row in sub_data if int(row["count_posts"]) > x] 

def sort_subs_by_avg_wo_outliers(subs: list[dict]) -> list[dict]:
    return sorted(subs, key=lambda row: float(row["avg_wo_outliers"]), reverse=True)

def find_all_posts_in_subreddit(subreddit_name: str) -> list[dict]:
    return [row for row in mapped_posts_data if row["subreddit"] == subreddit_name]

def percentage_of_posts_with_complexity_histogram(subreddit_name: str) -> dict:
    posts_in_subreddit = find_all_posts_in_subreddit(subreddit_name)
    complexity_counts = {}
    for post in posts_in_subreddit:
        complexity = math.floor(float(post["readability_index"]))
        if complexity not in complexity_counts:
            complexity_counts[complexity] = 0
        complexity_counts[complexity] += 1
    total_posts = len(posts_in_subreddit)
    percentage_histogram = {complexity: count / total_posts * 100 for complexity, count in complexity_counts.items()}

    # remove entries with less than 0.1% of posts
    percentage_histogram = {complexity: percentage for complexity, percentage in percentage_histogram.items() if percentage >= 0.1}

    return dict(sorted(percentage_histogram.items()))

def print_ordered_histogram(histogram: dict):
    for complexity, percentage in histogram.items():
        print(f"{complexity}: {percentage:.2f}%")

def top_10_subs_by_posts():
    top_10_subreddits = top_x_subreddits(10)
    for subreddit in top_10_subreddits:
        print(f"Subreddit: {subreddit}")

def top_and_bottom_ten_by_avg_wo_outliers():
    subs_with_more_than_1000_posts = subs_with_posts_greater_than(1000)
    # sort by avg_wo_outliers
    sorted_subs = sort_subs_by_avg_wo_outliers(subs_with_more_than_1000_posts)
    print("Number of Subreddits with more than 1000 posts:" + str(len(subs_with_more_than_1000_posts)))
    print("Top 10 Subreddits with more than 1000 posts sorted by avg_wo_outliers:")
    for subreddit in sorted_subs[:10]:
        print(f"{subreddit}")    
    print("Bottom 10 Subreddits with more than 1000 posts sorted by avg_wo_outliers:")
    for subreddit in sorted_subs[-10:]:
        print(f"{subreddit}")    

def percentage_histogram_for_3_top_subs():
    top_3_subreddits = ["AskReddit", "relationships", "leagueoflegends"]
    for subreddit in top_3_subreddits:
        print(f"Subreddit: {subreddit}")
        histogram = percentage_of_posts_with_complexity_histogram(subreddit)
        print_ordered_histogram(histogram)



# top_10_subs_by_posts()
# top_and_bottom_ten_by_avg_wo_outliers()
# percentage_histogram_for_3_top_subs()

# 100 most complex posts
sorted_posts = sorted(mapped_posts_data, key=lambda row: float(row["readability_index"]), reverse=True)
top_100_posts = sorted_posts[:100]
idx = 1
for post in top_100_posts:
    print(f"{idx}: {post['id']}, {post['subreddit']}, sCount: {post['sentence_count']}, wCount: {post['word_count']}, sylCount: {post['syllable_count']}, Complexity: {post['readability_index']}")
    idx += 1