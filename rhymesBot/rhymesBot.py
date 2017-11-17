import praw
from config import *
import requests

reddit = praw.Reddit(client_id=REDDIT_CLIENT,
   client_secret=REDDIT_SECRET,
   password=REDDIT_PASS,
   user_agent='bot searchs for words that rhyme by /u/rhymesBot',
   username=REDDIT_USER)

r = requests.get('https://api.datamuse.com/words?rel_rhy=floor')
print(r.json())
