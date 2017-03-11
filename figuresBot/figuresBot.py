from praw.models import MoreComments
from amazon.api import AmazonAPI
    
import collections  
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

def main():

    # Configuring account for bot
    reddit = praw.Reddit(client_id=REDDIT_CLIENT,
                     client_secret=REDDIT_SECRET,
                     password=REDDIT_PASS,
                     user_agent='amazon price search bot by /u/figuresBot',
                     username=REDDIT_USER)

    subreddit = reddit.subreddit(subredditName)

    # Streams each submission in subreddit
    for submission in subreddit.stream.submissions():
        print('Title - ' + submission.title)
        submission.comments.replace_more(limit=0)
        searchForLink(submission.comments.list())
        #time.sleep(60)
    

"""
Cycles through each comment in the submission and tries
to find an amazon url in a comment. We use regular
expressions to extract the ASIN number.
"""
def searchForLink (comments):
    for comment in comments:
        commentBody = comment.body
        if (re.search(urlRegex,commentBody)):
            reply(itemLookup(re.search(regex,commentBody).group(1)))
            
"""
Looks up the amazon item according to ASIN
"""
def itemLookup(asin):
    amazon = AmazonAPI(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,AWS_ASSOCIATE_TAG) 

    item = amazon.lookup(ItemId=asin)

    ProductInfo = collections.namedtuple('ProductInfo',
                                         ['title','amount','type'])
    return ProductInfo(item.title,item.price_and_currency[0],
                    item.price_and_currency[1])
    
"""
Generates a reply to the comment with information about
the amazon product
"""
def reply(p):
    print(p.title + ' ' + str(p.amount) + ' ' + p.type)

if __name__ == '__main__':
    main()
