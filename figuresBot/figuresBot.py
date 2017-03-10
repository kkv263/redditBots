from praw.models import MoreComments
from amazon.api import AmazonAPI
    
import os
import praw
import time
import re

# Variables
subredditName = 'test'
REDDIT_USER = os.environ['REDDIT_USER']
REDDIT_PASS = os.environ['REDDIT_PASS']
REDDIT_SECRET = os.environ['REDDIT_SECRET']
REDDIT_CLIENT = os.environ['REDDIT_CLIENT']
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_ASSOCIATE_TAG = os.environ['AWS_ASSOCIATE_TAG'] 

regex = re.compile('/([A-Z0-9]{10})')
urlRegex = re.compile('https?://www.amazon.com/([\\w-]+/)?(dp|gp/product|exec/obidos/asin)/(\\w+/)?(\\w{10})')

# Configuring account for bot
def main():
    reddit = praw.Reddit(client_id=REDDIT_CLIENT,
                     client_secret=REDDIT_SECRET,
                     password=REDDIT_PASS,
                     user_agent='amazon price search bot by /u/figuresBot',
                     username=REDDIT_USER)

    subreddit = reddit.subreddit(subredditName)
    
    print(reddit.user.me())
    print(subreddit)
   
    
    for submission in subreddit.stream.submissions():
        print(submission.title)
        submission.comments.replace_more(limit=0)
        searchKeyword(submission.comments.list())
        #time.sleep(2)
    

def searchKeyword (comments):
    print('Searching...')
    for comment in comments:
        commentBody = comment.body
        if (re.search(urlRegex,commentBody)):
            itemLookup(re.search(regex,commentBody).group(1))


def itemLookup(asin):
    amazon = AmazonAPI(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,AWS_ASSOCIATE_TAG) 

    item = amazon.lookup(ItemId=asin)

    print(item.title)
    print(item.price_and_currency)
    print(item.offer_url)

"""
TODO: def reply(title,price)
just basically replies to the comment with amazon information 
"""
if __name__ == '__main__':
    main()
