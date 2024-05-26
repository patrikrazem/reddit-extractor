import praw
import logging
import os
import json
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(name)s - %(message)s')
logger = logging.getLogger("Functions")

#function for step 1: get posts from subreddit (ideally step 1 would be find the appropriate ubsreddits...)
def get_top_threads_urls(reddit: praw.Reddit, subreddit_name, limit=10):
    logging.info(f"Fetching top {limit} threads from subreddit: {subreddit_name}")
    try:
        subreddit = reddit.subreddit(subreddit_name)
        top_threads = subreddit.top(limit=limit)
        base_url = "https://www.reddit.com"
        urls = [f"{base_url}{thread.permalink}" for thread in top_threads]        
        logging.info(f"Successfully fetched {len(urls)} threads from subreddit: {subreddit_name}")
        return urls
    except Exception as e:
        logging.error(f"An error occurred while fetching threads from subreddit: {subreddit_name} - {e}")
        return []

#patrikove funkcije za komentarje.
def get_paths(comment_text: str, replies: list, path: list = []) -> list:
    """Recursively extract all paths from a comment to the most nested comment."""

    path = path + [comment_text.replace("\n", " ").replace('"', "'")]
    if not replies:
        return [path]
    paths = []
    for reply in replies:
        paths.extend(get_paths(reply.body, reply.replies, path))
    return paths


# def store_post(post_id: str, post_text: str, paths: list):
#     """Store the post and all paths in a JSON file."""

#     start = f'    {{"content": "{post_text}"}}'
#     with open(f"output/post_{post_id}.json", "w") as f:
#         f.write("[\n")
#         f.write(start + ",\n")
#         for x in range(0, len(paths)):
#             nodes = [f'    {{"content": "{node}"}}' for node in paths[x]]
#             # nodes.insert(0, start)

#             f.write(",\n".join(nodes))
#             if x < len(paths) - 1:
#                 f.write(",\n")

#         f.write("\n]")

#     logger.info(f"Stored post {post_id} in output/post_{post_id}.json")


def store_post(post_id: str, post_text: str, paths: list, subreddit: str):
    """Store the post and all paths in a JSON file named after the subreddit."""

    file_path = f"output/{subreddit}.json"
    post_entry = {"content": post_text}

    if os.path.exists(file_path):
        # If the file exists, load the existing data
        with open(file_path, "r") as f:
            data = json.load(f)
    else:
        # If the file does not exist, start with an empty list
        data = []

    # Add the post entry
    data.append(post_entry)

    # Add the paths entries
    for path in paths:
        for node in path:
            data.append({"content": node})

    # Write the updated data back to the file
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"Stored post {post_id} in {file_path}")


def extract_comments(reddit: praw.Reddit, url: str, subreddit: str):
    """Extract comments from a Reddit post and store them in a JSON file."""

    logger.info(f"Extracting comments from {url} ...")

    # Retrieve post from Reddit
    post = reddit.submission(url=url)

    logger.info(f"Retrieved post {post.id}")

    # Extract post text and replace newlines and double quotes
    post_text = post.selftext.replace("\n", " ").replace('"', "'")

    # Get all comment trees available for this post
    post.comments.replace_more(limit=None)

    # Extract all available paths from the first comment to the most nested comment
    paths = []
    for comment in post.comments:
        paths.extend(get_paths(comment.body, comment.replies))

    # Store the post and all paths in a JSON file
    store_post(post.id, post_text, paths, subreddit)