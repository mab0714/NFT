"""from kcu import kjson
from reddit_scraper.reddit_scraper import RedditScraper

# posts = RedditScraper.get_posts('askreddit', max_count=10)

# print(len(posts))

id_ = 'uwwgf9'
post = RedditScraper.get_post(id_, comments_min_score=250)

j = post.json
del j['post_dict']
del j['comments_dict']

kjson.save(id_ + '.json', j)"""
import sys

import praw
from praw.models import MoreComments
from psaw import PushshiftAPI
import pandas as pd
import datetime as dt
from datetime import date, timedelta
keywords = sys.argv[1]

def getRedditData(keywords):
    api = PushshiftAPI()


    end_epoch = int(dt.datetime.now().timestamp())
    td = dt.timedelta(7)
    start_epoch = int((dt.datetime.now()-td).timestamp())
    api_request_generator = api.search_comments(q=keywords, after = start_epoch, before=end_epoch)
    depp_comments = pd.DataFrame([comment.d_ for comment in api_request_generator])
    f = open("C:\\Users\\Marvin\\Desktop\\NFT\\source\\data\\reddit_" + keywords.replace("+","") + ".txt", "w", encoding="utf8")
    reddit_string = ""

    for comment in depp_comments['body']:
        reddit_string += comment + "\n\n"
        f.write(comment + "\r\n")

    f.close()

    return reddit_string

"""
reddit = praw.Reddit(
    client_id="W4KWDSAgeeFFwC4ZWECJtw",
    client_secret="Kr7qGRWQeTSOf1rNmYarpMjK1_R5sQ",
    password="M@b040913",
    user_agent="dataminer by u/mab0714",
    username="mab0714",
)
"""

"""
url = "https://www.reddit.com/search/?q=johnny%20depp&type=comment"
submission = reddit.submission(url=url)
#submission = reddit.submission("3g1jfi")

for top_level_comment in submission.comments:
    if isinstance(top_level_comment, MoreComments):
        continue
    print(top_level_comment.body)
"""
#


#gen = api.search_comments(subreddit="subreddit1, subreddit2", q="johnny&depp")
#api_request_generator = api.search_submissions(q='Johnny Depp', score = ">1")
#depp_submissions = pd.DataFrame([submission.d_ for submission in api_request_generator])




#end_epoch=int(date.today())
#td = dt.timedelta(7)
#start_epoch=int((date.today-td))

reddit_string = getRedditData(keywords)

a=5