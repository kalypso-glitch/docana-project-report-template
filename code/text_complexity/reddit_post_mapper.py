# Takes a reddit post and maps it to a dictionary with desired fields for csv output

from nltk.tokenize import RegexpTokenizer

from typing import TypedDict

from code.text_complexity.compute_complexity import complexity_dictionary

class ReadabilityMetrics(TypedDict):
    id: str
    author: str
    subreddit_id: str
    subreddit: str

    sentence_count: int
    word_count: int
    syllable_count: int
    complex_words_count: int
    readability_index: int

def compute_reddit_readability_metrics_dict(item) -> ReadabilityMetrics:
    """
    Map a reddit post to a dictionary with desired fields for csv output.
    
    Args:
        item: A dictionary representing a reddit post.
    
    Returns:
        A dictionary with the desired fields for CSV output.
    """

    # print("author:", item.get("author"))
    # print("body:", item.get("body"))
    # print("content:", item.get("content"))
    # print("id:", item.get("id"))
    # print("normalizedBody:", item.get("normalizedBody"))
    # print("subreddit:", item.get("subreddit"))
    # print("subreddit_id:", item.get("subreddit_id"))
    # print("summary:", item.get("summary"))
    # print("-----")

    text = item.get("normalizedBody")
    if text is None:
        text = item.get("body")
    if text is None:
        text = ""

    readability_dictionary = complexity_dictionary(text)

    dictionary = {
        "id": item.get("id"),
        "author": item.get("author"),
        "subreddit_id": item.get("subreddit_id"),
        "subreddit": item.get("subreddit"),
    
        "sentence_count": readability_dictionary["sentence_count"],
        "word_count": readability_dictionary["word_count"],
        "syllable_count": readability_dictionary["syllable_count"],
        "complex_words_count": readability_dictionary["complex_words_count"],
        "readability_index": readability_dictionary["readability_index"]
    }


    return dictionary