from code.text_complexity.jsonReader import read_json_file
from code.text_complexity.reddit_post_mapper import compute_reddit_readability_metrics_dict

data_file_path = "data/corpus-webis-tldr-17.json"
destination_file_path = "results/mapped_reddit_posts.csv"

read_json_file(data_file_path, compute_reddit_readability_metrics_dict, destination_file_path)