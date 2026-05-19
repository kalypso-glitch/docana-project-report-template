from jsonReader import read_json_file
from reddit_post_mapper import map_reddit_post_language_complexity

data_file_path = "data/corpus-webis-tldr-17.json"
destination_file_path = "results/mapped_reddit_posts.csv"

read_json_file(data_file_path, map_reddit_post_language_complexity, destination_file_path, 5)