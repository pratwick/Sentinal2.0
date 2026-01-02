import os
import praw
from dotenv import load_dotenv

# Here we have loaded the environment variable
load_dotenv()

# Creating a fetch_reddit_data() function which would take topic and limit
def fetch_reddit_data(topic, limit=10):
    try:
        # first you need to call the praw API presenting all the stuff
        reddit = praw.Reddit(
            client_id = os.getenv('REDDIT_CLIENT_ID'),
            client_secret = os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent = os.getenv('REDDIT_USER_AGENT')
        )
        #REDDIT_USER_AGENT - This is for the USER_AGENT to support the metadata support
        
        # Always make the functionality of the reddit object which help us to connect to reddit account as readonly
        reddit.read_only = True # We are only giving the read only permission

        # Fetch post from reddit in read mode
        posts = []
        subreddit = reddit.subreddit('all') # all - with this we will consider all the subreddits in the account itself
        
        # Now we will use the search API which is used for subreddit, it will search for the specific topic and configurations
        for submission in subreddit.search(topic, sort='new', time_filter='all', limit=limit):
            posts.append({
                "title": submission.title,
                "content": submission.selftext or 'No content Available',# content will be taken by submission.selftext which is used to retrive the data from posting
                "url": submission.url
            })
        return posts
    except Exception as e:
        print(f'error fetching data from Reddit: {e}')
        return []

