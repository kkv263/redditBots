from praw.models import MoreComments
from amazon.api import AmazonAPI
from config import *
from urllib.parse import urlparse
from time import sleep
import collections, praw, re 

# Variables
subredditName = 'test'
asin_regex = re.compile('/([A-Z0-9]{10})')
locale_regex = re.compile('\..*?\.(.+)')
#es currently not working??
urlRegex = re.compile('https?://www.amazon.(com|de|co.uk|fr|ca|cn|it|in)/([\\w-]+/)?(dp|gp/product|exec/obidos/asin)/(\\w+/)?(\\w{10})')
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

"""
Cycles through each comment in the submission and tries
to find an amazon url in a comment. We also check if there
already is a comment made by the bot. If not, we use regular
expressions to extract the ASIN number and locale to prepare
the reply to the comment.
"""
def searchForLink (comments):
    for comment in comments:
        commentBody = comment.body
        botReplyExists = False
        data = re.search(urlRegex,commentBody)
        if (re.search(urlRegex,commentBody)):
            for reply in comment.replies.list():
                if (reply.author == REDDIT_USER):
                    botReplyExists = True
                    break;
                    
            if (comment.replies.__len__() == 0 or botReplyExists is False):
                locale = re.search(locale_regex,urlparse(data.group(0)).netloc).group(1)
                asin = re.search(asin_regex,commentBody).group(1)
                product = itemLookup(asin,pinRegion(locale))
                replyBody(product,asin,locale,comment)
                

"""
Determines the locale / region using the domain of the website
Does not support Brazil, Japan, and Mexico :(
"""
def pinRegion(locale):
    if (locale == 'com'):
        return 'US'
    elif (locale == 'co.uk'):
        return 'UK'
    elif (locale == 'cn'):
        return 'CN'
    elif (locale == 'fr'):
        return 'FR'
    elif (locale == 'de'):
        return 'DE'
    elif (locale == 'in'):
        return 'IN'
    elif (locale == 'it'):
        return 'IT'
    elif (locale == 'ca'):
        return 'CA'
    elif (locale == 'es'):
        return 'ES'

  
"""
Looks up the amazon item according to ASIN
"""
def itemLookup(asin,region):
    amazon = AmazonAPI(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,AWS_ASSOCIATE_TAG[region], Region = region) 
    item = amazon.lookup(ItemId=asin)
    sleep(10)

    ProductInfo = collections.namedtuple('ProductInfo',
                                         ['title','amount','type'])
    
    return ProductInfo(item.title,item.price_and_currency[0],
                    item.price_and_currency[1])
    
"""
Replies to the comment with the amazon link. Uses
Reddit's markdown formatting and provides information
about the amazon item.
"""    
def replyBody(product, asin, locale, comment):
    graphUrl = 'https://dyn.keepa.com/pricehistory.png?asin=' + asin + '&domain=' + locale
    title = ('**' + product.title + "**\n\n")
    chart = ('Current Listing | Currency |\n:-:|:-:\n' + str(product.amount) + ' | ' + product.type + '|\n')
    link = ('[Price History Graph - by Keepa.com](' + graphUrl + ')')
    
    comment.reply(title + chart + link)
    print('replied')
    
if __name__ == '__main__':
    main()
