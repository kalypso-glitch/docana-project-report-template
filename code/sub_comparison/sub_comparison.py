from code.sub_comparison.csv_reader import read_csv
import math

sub_data_path = "data/subreddit_stats.csv"
sub_data = read_csv(sub_data_path)

mapped_posts_path = "data/mapped_reddit_posts.csv"
mapped_posts_data = read_csv(mapped_posts_path)


# by number of posts
def top_x_subreddits(x: int) -> list[dict]:
    sorted_data = sorted(sub_data, key=lambda row: int(row["count_posts"]), reverse=True)
    return sorted_data[:x]

def subs_with_posts_greater_than(x: int) -> list[dict]:
    return [row for row in sub_data if int(row["count_posts"]) > x] 

def sort_subs_by_avg_capped_25(subs: list[dict]) -> list[dict]:
    return sorted(subs, key=lambda row: float(row["avg_capped_25"]), reverse=True)

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

    # remove entries with complexity higher than 20
    percentage_histogram = {complexity: percentage for complexity, percentage in percentage_histogram.items() if complexity <= 20}

    return dict(sorted(percentage_histogram.items()))

def print_formatted_ordered_histogram(histogram: dict):
    # for complexity, percentage in histogram.items():
        # print(f"{complexity}: {percentage:.2f}%")
    excel_string = "\n".join(
        f"{complexity},{percentage:.2f}%"
        for complexity, percentage in histogram.items()
    )
    print(excel_string)

def top_10_subs_by_posts():
    top_10_subreddits = top_x_subreddits(10)
    for subreddit in top_10_subreddits:
        print(f"Subreddit: {subreddit}")

def top_and_bottom_ten_by_avg_capped_25():
    subs_with_more_than_1000_posts = subs_with_posts_greater_than(1000)
    # sort by avg_capped_25
    sorted_subs = sort_subs_by_avg_capped_25(subs_with_more_than_1000_posts)
    print("Number of Subreddits with more than 1000 posts:" + str(len(subs_with_more_than_1000_posts)))
    print("Top 10 Subreddits with more than 1000 posts sorted by avg_capped_25:")
    for subreddit in sorted_subs[:10]:
        print(f"{subreddit}")    
    print("Bottom 10 Subreddits with more than 1000 posts sorted non-ascendingly by avg_capped_25:")
    least_complex_subs = sorted_subs[-10:]
    for subreddit in least_complex_subs[::-1]:
        print(f"{subreddit}")    

def percentage_histogram_for_3_top_subs():
    top_3_subreddits = ["AskReddit", "relationships", "leagueoflegends"]
    for subreddit in top_3_subreddits:
        print(f"Subreddit: {subreddit}")
        histogram = percentage_of_posts_with_complexity_histogram(subreddit)
        print_formatted_ordered_histogram(histogram)

def average_complex_words_per_100(subreddit_name: str) -> float:
    posts_in_subreddit = find_all_posts_in_subreddit(subreddit_name)
    total_complex_words = sum(float(post["complex_words_count"]) for post in posts_in_subreddit)
    total_words = sum(float(post["word_count"]) for post in posts_in_subreddit)
    if total_words == 0:
        return 0.0
    return (total_complex_words / total_words) * 100

def average_sentence_length(subreddit_name: str) -> float:
    posts_in_subreddit = find_all_posts_in_subreddit(subreddit_name)
    total_sentences = sum(float(post["sentence_count"]) for post in posts_in_subreddit)
    total_words = sum(float(post["word_count"]) for post in posts_in_subreddit)
    if total_sentences == 0:
        return 0.0
    return total_words / total_sentences

def print_average_complex_word_sentence_length_top_3():
    top_3_subreddits = ["AskReddit", "relationships", "leagueoflegends"]
    for subreddit in top_3_subreddits:
        avg_complex_words = average_complex_words_per_100(subreddit)
        avg_sentence_length = average_sentence_length(subreddit)
        print(f"Subreddit: {subreddit}, Average Complex Words per 100: {avg_complex_words:.2f}, Average Sentence Length: {avg_sentence_length:.2f}")

def percentage_histogram_for_most_complex_subreddit():
    most_complex_subreddit = "AskHistorians"
    print(f"Most complex subreddit: {most_complex_subreddit}")
    histogram = percentage_of_posts_with_complexity_histogram(most_complex_subreddit)
    print_formatted_ordered_histogram(histogram)

def print_average_complex_word_sentence_length_most_complex():
    top_subreddit = "AskHistorians"
    avg_complex_words = average_complex_words_per_100(top_subreddit)
    avg_sentence_length = average_sentence_length(top_subreddit)
    print(f"Subreddit: {top_subreddit}, Average Complex Words per 100: {avg_complex_words:.2f}, Average Sentence Length: {avg_sentence_length:.2f}")

def complexity_to_popularity_correlation():
    # create a list of tuples (complexity, popularity) for each subreddit
    complexity_popularity = []
    relevant_subreddits = subs_with_posts_greater_than(50)
    for subreddit in relevant_subreddits:
        complexity = float(subreddit["avg_capped_25"])
        popularity = int(subreddit["count_posts"])
        complexity_popularity.append((complexity, popularity))
    # sort by complexity
    complexity_popularity.sort(key=lambda x: x[0], reverse=True)
    return complexity_popularity

def print_excel_ready_complexity_to_popularity_correlation_to_csv(file_path: str = "results/complexity_to_popularity_correlation.csv"):
    correlation_data = complexity_to_popularity_correlation()
    excel_string = "\n".join(
        f"{complexity},{popularity}"
        for complexity, popularity in correlation_data
    )
    with open(file_path, "w") as f:
        f.write(excel_string)
    print(f"Complexity to popularity correlation data written to {file_path}")

def standard_deviation_of_posts_in_subreddit(subreddit_name: str) -> float:
    posts_in_subreddit = find_all_posts_in_subreddit(subreddit_name)
    complexities = [float(post["readability_index"]) for post in posts_in_subreddit]
    if len(complexities) == 0:
        print(f"No posts found in subreddit: {subreddit_name}")
        return 0.0
    mean = sum(complexities) / len(complexities)
    variance = sum((x - mean) ** 2 for x in complexities) / len(complexities)
    return math.sqrt(variance)

def standard_deviation_of_top_10_subreddits():
    top_10_subreddits = top_x_subreddits(10)
    for subreddit in top_10_subreddits:
        std_dev = standard_deviation_of_posts_in_subreddit(subreddit["subreddit"])
        print(f"Subreddit: {subreddit['subreddit']}, Standard Deviation of Readability Index: {std_dev:.2f}")

def standard_deviation_of_most_complex_subreddits():
    top_10_subreddits = ["argentina", "AskHistorians", "philosophy", "askscience", "Anarchism", "PoliticalDiscussion", "history", "Anarcho_Capitalism", "Economics",  "europe"]
    for subreddit in top_10_subreddits:
        std_dev = standard_deviation_of_posts_in_subreddit(subreddit)
        print(f"Subreddit: {subreddit}, Standard Deviation of Readability Index: {std_dev:.2f}")

def standard_deviation_of_least_complex_subreddits():
    least_complex_subreddits = ["breakingmom", "Random_Acts_Of_Amazon", "circlejerk", "cripplingalcoholism", "C25K", "golf", "amiugly", "TalesFromRetail", "discgolf", "TalesFromYourServer"]
    for subreddit in least_complex_subreddits:
        std_dev = standard_deviation_of_posts_in_subreddit(subreddit)
        print(f"Subreddit: {subreddit}, Standard Deviation of Readability Index: {std_dev:.2f}")

def avg_complexity_of_subreddit(subreddit_name: str) -> float:
    posts_in_subreddit = find_all_posts_in_subreddit(subreddit_name)
    complexities = [float(post["readability_index"]) for post in posts_in_subreddit]
    complexities_max_25 = [c for c in complexities if c <= 25]
    if len(complexities) == 0:
        print(f"No posts found in subreddit: {subreddit_name}")
    print(f"Average complexity in {subreddit_name}: {sum(complexities) / len(complexities)}, ({len(complexities)} posts) (sum of complexities: {sum(complexities)})")
    print(f"Average complexity in {subreddit_name} (capped at 25): {sum(complexities_max_25) / len(complexities_max_25)} ({len(complexities_max_25)} posts capped at 25) (sum of complexities capped at 25: {sum(complexities_max_25)})")


# top_10_subs_by_posts()
# top_and_bottom_ten_by_avg_capped_25()
# percentage_histogram_for_3_top_subs()
# print_average_complex_word_sentence_length_top_3()
# percentage_histogram_for_most_complex_subreddit()
# print_average_complex_word_sentence_length_most_complex()
# print_excel_ready_complexity_to_popularity_correlation_to_csv()
# standard_deviation_of_top_10_subreddits()
standard_deviation_of_most_complex_subreddits()
print()
standard_deviation_of_least_complex_subreddits()



# Debug
# avg_complexity_of_subreddit("AskHistorians")
# avg_complexity_of_subreddit("circlejerk")





# python -m code.sub_comparison.sub_comparison

# 100 most complex posts
# sorted_posts = sorted(mapped_posts_data, key=lambda row: float(row["readability_index"]), reverse=True)
# top_100_posts = sorted_posts[:100]
# idx = 1
# for post in top_100_posts:
#     print(f"{idx}: {post['id']}, {post['subreddit']}, sCount: {post['sentence_count']}, wCount: {post['word_count']}, sylCount: {post['syllable_count']}, Complexity: {post['readability_index']}")
#     idx += 1