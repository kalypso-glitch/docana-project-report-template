# Takes a reddit post and maps it to a dictionary with desired fields for csv output

from nltk.tokenize import RegexpTokenizer

def map_reddit_post_language_complexity(item):
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

    
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)


    return {
        "author": item.get("author"),
        "id": item.get("id"),
        "subreddit": item.get("subreddit"),
        "subreddit_id": item.get("subreddit_id"),
    }