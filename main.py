#%%
import logging
import praw
from environs import Env
#%%
# Create an instance of Env
env = Env()

# Read environment variables from .env file (if it exists)
env.read_env()

# Extract environment variables
CLIENT_ID = (env.str("REDDIT_CLIENT_ID"),)
CLIENT_SECRET = (env.str("REDDIT_CLIENT_SECRET"),)
USERNAME = (env.str("REDDIT_USERNAME"),)
PASSWORD = (env.str("REDDIT_PASSWORD"),)
USER_AGENT = env.str("REDDIT_USER_AGENT")

TARGETED_URLS = [
    "https://www.reddit.com/r/funny/comments/1crnefz/a_man_returns_from_the_doctor_and_tells_his_wife/",
    "https://www.reddit.com/r/AmItheAsshole/comments/1cu5vzu/aita_for_sticking_to_my_word_and_not_giving_my/"
]

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(name)s - %(message)s')
logger = logging.getLogger("Main")


def get_paths(comment_text: str, replies: list, path: list = []) -> list:
    """Recursively extract all paths from a comment to the most nested comment."""

    path = path + [comment_text.replace("\n", " ").replace('"', "'")]
    if not replies:
        return [path]
    paths = []
    for reply in replies:
        paths.extend(get_paths(reply.body, reply.replies, path))
    return paths


def store_post(post_id: str, post_text: str, paths: list):
    """Store the post and all paths in a JSON file."""

    start = f'    {{"content": "{post_text}"}}'
    with open(f"output/post_{post_id}.json", "w") as f:
        f.write("[\n")
        f.write(start + ",\n")
        for x in range(0, len(paths)):
            nodes = [f'    {{"content": "{node}"}}' for node in paths[x]]
            # nodes.insert(0, start)

            f.write(",\n".join(nodes))
            if x < len(paths) - 1:
                f.write(",\n")

        f.write("\n]")

    logger.info(f"Stored post {post_id} in output/post_{post_id}.json")


def extract_comments(reddit: praw.Reddit, url: str):
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
    store_post(post.id, post_text, paths)


if __name__ == "__main__":
    # Initialize Reddit client
    reddit = praw.Reddit(
        client_id=env.str("REDDIT_CLIENT_ID"),
        client_secret=env.str("REDDIT_CLIENT_SECRET"),
        username=env.str("REDDIT_USERNAME"),
        password=env.str("REDDIT_PASSWORD"),
        user_agent=env.str("REDDIT_USER_AGENT"),
    )

    for url in TARGETED_URLS:
        extract_comments(reddit, url)
