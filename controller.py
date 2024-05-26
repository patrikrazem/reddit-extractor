#this is where we initiate our reddit instance and call all the other functions. 
#basically what we run to get the result
import praw
from environs import Env
import logging
from functions import get_top_threads_urls, extract_comments, get_paths, store_post
import time

env = Env()

# Read environment variables from .env file (if it exists)
env.read_env()

# Extract environment variables
CLIENT_ID = (env.str("REDDIT_CLIENT_ID"),)
CLIENT_SECRET = (env.str("REDDIT_CLIENT_SECRET"),)
USERNAME = (env.str("REDDIT_USERNAME"),)
PASSWORD = (env.str("REDDIT_PASSWORD"),)
USER_AGENT = env.str("REDDIT_USER_AGENT")

#crawling parameters
subreddit='BDSM'
limit=10
pause=2

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(name)s - %(message)s')
logger = logging.getLogger("Controller")

#initialization
reddit = praw.Reddit(
    client_id=env.str("REDDIT_CLIENT_ID"),
    client_secret=env.str("REDDIT_CLIENT_SECRET"),
    username=env.str("REDDIT_USERNAME"),
    password=env.str("REDDIT_PASSWORD"),
    user_agent=env.str("REDDIT_USER_AGENT"),
)

subreddit_thread_urls = get_top_threads_urls(reddit, subreddit, limit=limit)

for url in subreddit_thread_urls:
    time.sleep(pause)
    extract_comments(reddit, url, subreddit)
