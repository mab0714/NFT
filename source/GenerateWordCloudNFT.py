#!/usr/bin/env python

# libraries
import datetime
import glob
import os
import sys
import token
import random
import cv2
import tweepy
import pandas as pd
import re
# importing the module
import wikipedia
import pandas as pd
import sys
import DuckDuckGoImages as ddg
import emoji
import nltk
import preprocessor as p
from bs4 import BeautifulSoup
from matplotlib.animation import FuncAnimation
from nltk.tokenize import WordPunctTokenizer
from scipy.ndimage import gaussian_gradient_magnitude
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from os.path import exists
from newsapi import NewsApiClient
from newspaper import Article
import re
import math
from nytimesarticle import articleAPI
import requests
import json
from newspaper import fulltext
from psaw import PushshiftAPI
from pyyoutube import Api
from youtubesearchpython import *
from facebook_page_scraper import Facebook_scraper
import logging

# Method to clean background from image
def clean_background(keywords):
    print("Removing background for: " + keywords)
    logging.info("Removing background for: " + keywords)
    try:
        cmd = 'backgroundremover -i images//' + keywords + '.jpg -o images//' + keywords + '_Transparent.png'
        os.system('cmd /c ' + cmd)

        # load image with alpha channel.  use IMREAD_UNCHANGED to ensure loading of alpha channel
        image = cv2.imread('images/' + keywords + '_Transparent.png', cv2.IMREAD_UNCHANGED)
        cv2.imwrite("images\\" + keywords + "_Transparent.jpg", image)

        if image is None:
            return

        # make mask of where the transparent bits are
        trans_mask = image[:, :, 3] == 0

        # replace areas of transparency with white and not transparent
        image[trans_mask] = [255, 255, 255, 255]

        # new image without alpha channel...
        new_img = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

        cv2.imwrite("images\\" + keywords + "_Final.jpg", new_img)
        os.remove('images\\' + keywords + '_Transparent.png')
    except Exception as e:
        logging.info("Error with clean_background:" + str(e))
        pass

# Method to clean tweets
def cleaning_tweets(t,token):
    try:
        re_list = ['(https?://)?(www\.)?(\w+\.)?(\w+)(\.\w+)(/.+)?', '@[A-Za-z0-9_]+', '#']
        combined_re = re.compile('|'.join(re_list))

        regex_pattern = re.compile(pattern="["
                                           u"\U0001F600-\U0001F64F"  # emoticons
                                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                           "]+", flags=re.UNICODE)
        del_amp = BeautifulSoup(t, 'lxml')
        del_amp_text = del_amp.get_text()
        hashtags = extract_hashtags(del_amp_text)
        del_link_mentions = re.sub(combined_re, '', del_amp_text)
        del_emoticons = re.sub(regex_pattern, '', del_link_mentions)
        lower_case = del_emoticons.lower()
        words = token.tokenize(lower_case)
        result_words = [x for x in words if len(x) > 2]
        #result_words.append(extract_hashtags)
        return (" ".join(result_words)).strip(), hashtags
    except Exception as e:
        logging.info("Error with cleaning_tweets:" + str(e))
        return " "

def extract_hashtags(tweets):
    hashtags = [tweet for tweet in tweets.split() if "#" in tweet]
    return hashtags

def clean_text(text):
    '''
    Utility function to clean text by removing links, special characters
    using simple regex statements.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())

# Method to store tweets in CSV
def keyword_to_csv(api, keyword, twitter_search, recent):
    print("Converting Keywords to CSV for keyword: " + keyword + " and search: " + twitter_search + " from recent: " + str(recent) + " tweets")
    logging.info("Converting Keywords to CSV for keyword: " + keyword + " and search: " + twitter_search + " from recent: " + str(recent) + " tweets")
    try:
        tweets = tweepy.Cursor(api.search, q=twitter_search + "-filter:retweets", lang='en').items(recent)
        #tweets_list = [[(tweet.favorite_count+tweet.retweet_count)*tweet.text] for tweet in tweets]
        tweets_list = []
        for tweet in tweets:
            try:
                for url in tweet.entities['urls']:
                    web_url = url['expanded_url']

                    if len(web_url) > 0 and not web_url.__contains__('t.co') and not web_url.__contains__('twitter.com'):
                        article = Article(web_url)
                        article.download()
                        article.parse()
                        article.nlp()
                        title = article.title
                        text = clean_text(article.text)
                        keywords = article.keywords
                        summary = clean_text(article.summary)
                        tweets_list.append(max(tweet.favorite_count+tweet.retweet_count,1)*(tweet.text + "\n" + text + "\n" + summary + "\n" + keywords + "\n" + title))
                    else:
                        tweets_list.append(max(tweet.favorite_count+tweet.retweet_count,1)*tweet.text)
            except Exception as e:
                logging.info("Error with keyword_to_csv:" + str(e))
                tweets_list.append(max(tweet.favorite_count+tweet.retweet_count,1)*tweet.text)
                continue

        df = pd.DataFrame(tweets_list, columns=['Text'])
        df.to_csv('{}.csv'.format(keyword), sep=',', index=False)
    except BaseException as e:
        logging.info("Error with keyword_to_csv:" + str(e))
        datetime.time.sleep(3)

# Method to stream tweets
def getTwitterData(keywords,twitter_search,recent):
    print("Getting twitter data for keywords: " + keywords + " from recent: " + str(recent) + " tweets")
    logging.info("Getting twitter data for keywords: " + keywords + " from recent: " + str(recent) + " tweets")

    # search twitter
    # twitter info
    access_token = "4192621779-R2yag5NcDn0aisOAAPmhEoaMfneL39hJSneU1ev"
    access_token_secret = "LKgkU8tNxs45gLiHN6zPOU57VXp6338tdvCxb6tZc6gkw"
    consumer_key = "kk32njRRde69Jqtq4l2e7dOT3"
    consumer_secret = "IQtaWbqdNXPgVNCEqdbn9x1fjKyMX0mLulEzK1BYkaM4F9OVJB"

    # twitter api
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    keyword = '#' + keywords + "-filter:retweets"
    keyword_to_csv(api, keyword,twitter_search, recent)

    # gather words
    df = pd.read_csv("./#" + keywords + "-filter:retweets.csv")
    pd.options.display.max_colwidth = 200
    df.head()

    df.shape

    token = WordPunctTokenizer()

    # clean tweets
    cleaned_tweets = []
    new_tags = ""
    for i in range(0, 3000):
        """
        if ((i + 1) % 100 == 0):
            print("Tweets {} of {} have been processed".format(i + 1, 3000))
        """
        try:
            words,hashtags = cleaning_tweets((df.Text[i]),token)
            cleaned_tweets.append(words)
            for hashtag in hashtags:
                if (hashtag.replace("#","").replace(".","").lower() not in twitter_search.lower()):
                    if (hashtag.replace("#","").replace(".","").lower() not in new_tags.lower()):
                        new_tags += hashtag.replace("#","") + " OR "
        except Exception as e:
            logging.info("Error with getTwitterData:" + str(e))
            continue

    # build string of words from twitter
    return pd.Series(cleaned_tweets).str.cat(sep=' '), new_tags.rstrip(" OR")

# Method to scrape Wikipedia
def getWikipediaData(keywords,recent):
    print ("Getting Wikipedia data for: " + keywords)
    logging.info("Getting Wikipedia data for: " + keywords)

    results = wikipedia.search(keywords, results=recent)
    page_objects = []
    for result in results:
        try:
            page_objects.append(wikipedia.page(result))
        except Exception as e:
            logging.info("Error with getWikipediaData:" + str(e))
            continue

    wiki_string = ""
    for object in page_objects:
        wiki_string += object.content
    return wiki_string

# Method to get data from a file
def getFileData(keywords):
    print ("Getting File data for: " + keywords)
    logging.info("Getting File data for: " + keywords)
    files = []
    file_string = ""
    for file in glob.glob("data\\*" + keywords + "*"):
        files.append(file)

    for file in files:
        try:
            #file = "data\\" + keywords + ".txt"
            f = open(file, "r", encoding='utf-8')
            lines = f.readlines()



            for line in lines:
                file_string += line
            f.close()
        except Exception as e:
            logging.info("Error with getFileData:" + str(e))
            continue

    return file_string

# Method to get single page from NewsAPI
def getPage(keywords, page, text, f, newsapi):

    td = datetime.timedelta(7)
    start_day = datetime.date.today() - td
    end_day = datetime.date.today()

    all_articles = newsapi.get_everything(
        q=keywords,
        language='en',
        page=page,
        sort_by='relevancy',
        from_param=start_day,
        to=end_day
    )
    numPages = math.ceil(all_articles['totalResults'] / len(all_articles['articles']))
    for article in all_articles['articles']:
        web_url = article['url']
        data = ""
        try:
            article = Article(web_url)
            article.download()
            article.parse()
            article.nlp()
            title = article.title
            text = clean_text(article.text)
            keywords = article.keywords
            summary = clean_text(article.summary)
            data += "\n" + text + "\n" + summary + "\n" + ' '.join(keywords) + "\n" + title
            f.write(data + "\n")
        except Exception as e:
            logging.info("Error with getPage:" + str(e))
            continue
    return numPages, data

# Method to scrape NewsAPI
def getNewsApiData(keywords):
    print("Getting NewsApi data for: " + keywords)
    logging.info("Getting NewsApi data for: " + keywords)
    newsapi = NewsApiClient(api_key='28c66e5fc20e435298767d2a4a899e03')
    data = ""
    f = open("C:\\Users\\Marvin\\Desktop\\NFT\\source\\data\\newsapi_" + keywords + ".txt", "a", encoding="utf8")

    numPages, text = getPage(keywords, 1, "", f, newsapi)
    data = text
    for page in range(numPages):
        if page > 1:
            try:
                numPages, text = getPage(keywords, page, text, f, newsapi)
                data += "\n" + text
            except Exception as e:
                logging.info("Error with getNewsApiData:" + str(e))
                continue

    f.close()
    return data

# Method to get NYTimes articles
def getNYTimesData(keywords):
    print("Getting NYTimes data for: " + keywords)
    logging.info("Getting NYTimes data for: " + keywords)

    #api = articleAPI("ahIYn6AjQ1iQMIkrYGI7GGIaL1jkyCw8")
    r = requests.get(
        'https://api.nytimes.com/svc/search/v2/articlesearch.json?query=' + keywords + '&api-key=ahIYn6AjQ1iQMIkrYGI7GGIaL1jkyCw8')
    datastore = json.loads(r.text)

    f = open("C:\\Users\\Marvin\\Desktop\\NFT\\source\\data\\nyt_" + keywords + ".txt", "a", encoding="utf8")
    data = ""
    for doc in datastore['response']['docs']:
        web_url = doc['web_url']
        try:
            article = Article(web_url)
            article.download()
            article.parse()
            article.nlp()
            title = article.title
            text = clean_text(article.text)
            keywords = article.keywords
            summary = clean_text(article.summary)
            data += "\n" + text + "\n" + summary + "\n" + ' '.join(keywords) + "\n" + title
            f.write(data + "\n")

        except Exception as e:
            logging.info("Error with getNYTimesData:" + str(e))
            continue

    return data
    f.close()

# Method to get Reddit posts
def getRedditData(keywords):
    print("Getting Reddit data for: " + keywords)
    logging.info("Getting Reddit data for: " + keywords)

    try:
        api = PushshiftAPI()

        end_epoch = int(datetime.datetime.now().timestamp())
        td = datetime.timedelta(7)
        start_epoch = int((datetime.datetime.now() - td).timestamp())
        api_request_generator = api.search_comments(q=keywords, after=start_epoch, before=end_epoch)
        comments = pd.DataFrame([comment.d_ for comment in api_request_generator])
        f = open("C:\\Users\\Marvin\\Desktop\\NFT\\source\\data\\reddit_" + keywords.replace("+", "") + ".txt", "a",
                 encoding="utf8")
        reddit_string = ""

        for comment in comments['body']:
            reddit_string += comment + "\n\n"
            f.write(comment + "\r\n")

        f.close()
    except Exception as e:
        print("Error with getRedditData:" + str(e))
        logging.info("Error with getRedditData:" + str(e))
        pass

    return reddit_string

# Method to get Youtube comments
def getYouTubeData(keywords,recent):
    print("Getting YouTube data for: " + keywords)
    logging.info("Getting YouTube data for: " + keywords)

    api = Api(api_key="AIzaSyDkRxErB1pDXHJK7BkLJnVqgnvx0FHyQWE")
    r = api.search_by_keywords(q=keywords, search_type=["comments"], count=3, limit=recent)
    f = open("C:\\Users\\Marvin\\Desktop\\NFT\\source\\data\\youtube_" + keywords.replace("+", "") + ".txt", "w",
             encoding="utf8")
    youtube_string = ""
    try:
        if r.items is not None:
            for item in r.items:
                video_id = item.id.videoId
                comments = Comments(video_id)
                i = 0
                while comments.hasMoreComments & i < recent:
                    try:
                        if comments.comments['result'] is not None:
                            for comment in comments.comments['result']:
                                if (((comment['content'] is not None) | (len(comment['content']) > 0)) & (comment['replyCount'] is not None)):
                                    #try:
                                    youtube_string += (max(comment['replyCount'], 1)) * (comment['content'])
                                    f.write((max(comment['replyCount'], 1)) * (comment['content']) + "\r\n")
                                    #except Exception as e:
                                    #    logging.info("Error with getYouTubeData:" + str(e))
                                    #    youtube_string += comment['content']
                                    #    f.write(comment['content'] + "\r\n")
                                else:
                                    youtube_string += comment['content']
                                    f.write(comment['content'] + "\r\n")
                                i += 1
                    except Exception as e:
                        continue
                    comments.getNextComments()
    except Exception as e:
        pass
    f.close()

    return youtube_string

# Method to get Facebook posts
def getFacebookData(keywords, recent):
    print("Getting Facebook data for: " + keywords)
    logging.info("Getting Facebook data for: " + keywords)
    posts_count = int(recent/25)
    browser = "chrome"

    f = open("C:\\Users\\Marvin\\Desktop\\NFT\\source\\data\\facebook_" + keywords.replace("+", "") + ".txt", "a",
             encoding="utf8")

    for page_name in keywords.split(','):
        facebook_ai = Facebook_scraper(page_name, posts_count, browser)

        json_data = facebook_ai.scrap_to_json()
        data_dict = json.loads(json_data)

        facebook_string = ""
        for key in data_dict:
            if (len(data_dict[key]['content']) > 0 & len(data_dict[key]['reaction_count']) > 0):
                try:
                    f.write((max(data_dict[key]['reaction_count'], 1)) * (data_dict[key]['content'] + "\n"))
                    facebook_string += (max(data_dict[key]['reaction_count'], 1)) * (data_dict[key]['content'] + "\n")
                except Exception as e:
                    logging.info("Error with getFacebookData:" + str(e))
                    f.write(data_dict[key]['content'] + "\n")
                    facebook_string += data_dict[key]['content']

    f.close()
    return facebook_string

def getData(source,keywords,twitter_search,recent,keywordswithspace,fbpage):
    words = ""
    filenamepostfix = ""
    # Get Twitter Data
    if (source.__contains__('twitter') or source.__contains__('all')):
        try:
            twitter_string, tags = getTwitterData(keywords, twitter_search, recent)

            #if (len(tags) > 0):
            #     new_twitter_string, tags = getTwitterData(keywords, tags, recent)

            #twitter_string += "\n" + new_twitter_string

            f = open("C:\\Users\\Marvin\\Desktop\\NFT\\source\\data\\twitter_" + keywords + ".txt", "a",
                     encoding="utf8")
            f.write(twitter_string)
            f.close()
            words = twitter_string
            filenamepostfix = "Twitter"
        except Exception as e:
            logging.info("Error with twitter:" + str(e))
            pass
    # Get Wikipedia Data
    if (source.__contains__('wiki') or source.__contains__('all')):
        try:
            wiki_string = getWikipediaData(keywords, recent)
            f = open("C:\\Users\\Marvin\\Desktop\\NFT\\source\\data\\wiki_" + keywords + ".txt", "a", encoding="utf8")
            f.write(wiki_string)
            f.close()
            words = wiki_string
            filenamepostfix = "Wiki"
        except Exception as e:
            logging.info("Error with wiki:" + str(e))
            pass
    # Get File Data
    if (source.__contains__('file') or source.__contains__('all')):
        try:
            file_string = getFileData(keywords)
            words = file_string
            filenamepostfix = "File"
        except Exception as e:
            logging.info("Error with file:" + str(e))
            pass
    # Get NewsAPI data
    if (source.__contains__('newsapi') or source.__contains__('all')):
        try:
            newsapi_string = getNewsApiData(keywords)
            words = newsapi_string
            filenamepostfix = "NewsApi"
        except Exception as e:
            logging.info("Error with NewsApi:" + str(e))
            pass
    # Get NYTimes data
    if (source.__contains__('nytimes') or source.__contains__('all')):
        try:
            nytimes_string = getNYTimesData(keywordswithspace)
            words = nytimes_string
            filenamepostfix = "NYTimes"
        except Exception as e:
            logging.info("Error with NYTimes:" + str(e))
            pass
    # Get Reddit data
    if (source.__contains__('reddit') or source.__contains__('all')):
        try:
            reddit_string = getRedditData(keywordswithspace)
            words = reddit_string
            filenamepostfix = "Reddit"
        except Exception as e:
            logging.info("Error with Reddit:" + str(e))
            pass
    # Get Youtube data
    if (source.__contains__('youtube') or source.__contains__('all')):
        try:
            youtube_string = getYouTubeData(keywords, recent)
            words = youtube_string
            filenamepostfix = "Youtube"
        except Exception as e:
            logging.info("Error with Youtube:" + str(e))
            pass

    if (source.__contains__('facebook') or source.__contains__('all')):
        try:
            if (len(fbpage) > 0):
                facebook_string = getFacebookData(fbpage, recent)
                words = facebook_string
                filenamepostfix = "Facebook"
        except Exception as e:
            logging.info("Error with Facebook:" + str(e))
            pass
    # Combine words
    if (source.__contains__('all')):
        all_string = twitter_string + "\n" + wiki_string + "\n" + file_string + "\n" + newsapi_string + "\n" \
                     + nytimes_string + "\n" + reddit_string + "\n" + youtube_string + "\n" + facebook_string

        token = WordPunctTokenizer()
        all_string = token.tokenize(all_string.lower())
        """
        f = open("C:\\Users\\Marvin\\Desktop\\NFT\\source\\data\\all_" + keywords + ".txt", "a", encoding="utf8")

        all_string = [x for x in all_string if len(x) > 2]
        all_string = " ".join(all_string)
        f.write(all_string)
        f.close()
        """
        words = all_string
        filenamepostfix = "All"
    return words,filenamepostfix


def main(argv):
    # Logging
    logging.basicConfig(level=logging.INFO, filename='logs/run.log', filemode='a',
                        format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                        datefmt='%Y-%m-%d:%H:%M:%S',                        )
    # input keyword
    source = sys.argv[1]
    keywords = sys.argv[2]
    keywordswithspace = sys.argv[3]
    hashtags = sys.argv[4]
    twitter_search = ""
    for hashtag in hashtags.split(','):
        twitter_search += hashtag + ' OR '

    twitter_search = twitter_search.rstrip(' OR ')

    recent = int(sys.argv[5])
    font = sys.argv[6]
    usecolor = sys.argv[7]
    fbpage = sys.argv[8]

    print("source: " + source)
    print("keywords: " + keywords)
    print("keywordswithspace: " + keywordswithspace)
    print("hashtags: " + hashtags)
    print("twitter_search: " + twitter_search)
    print("recent: " + str(recent))
    print("font: " + font)
    print("usecolor: " + usecolor)
    print("fbpage: " + fbpage)

    logging.info("source: " + source)
    logging.info("keywords: " + keywords)
    logging.info("keywordswithspace: " + keywordswithspace)
    logging.info("hashtags: " + hashtags)
    logging.info("twitter_search: " + twitter_search)
    logging.info("recent: " + str(recent))
    logging.info("font: " + font)
    logging.info("usecolor: " + usecolor)
    logging.info("fbpage: " + fbpage)

    # Download Picture

    # Remove Background
    try:
        clean_background(keywords)
    except Exception as e:
        logging.info("Error with clean_background:" + str(e))
        pass

    # https://dashboard.photoroom.com/accounts/login/
    # https://pypi.org/project/backgroundremover/

    twitter_string = ""
    wiki_string = ""
    file_string = ""
    newsapi_string = ""
    nytimes_string = ""
    reddit_string = ""
    youtube_string = ""
    facebook_string = ""
    all_string = ""

    words = ""
    filenamepostfix = ""

    # Test
    all = ['twitter','wiki','file','newsapi','nytimes','reddit','youtube','facebook']
    if source.__contains__('all'):
        temp = ""
        tempfix = ""
        for source in all:
            temp, tempfix = getData(source, keywords, twitter_search, recent, keywordswithspace, fbpage)
            words += temp + "\n"
            filenamepostfix = "All"
    else:
        selectedSources = source.split(',')
        temp = ""
        tempfix = ""
        for source in selectedSources:
            temp, tempfix = getData(source, keywords, twitter_search, recent, keywordswithspace, fbpage)
            words += temp + "\n"
            filenamepostfix += tempfix + "-"
            #words, filenamepostfix = getData(source,keywords,twitter_search,recent,keywordswithspace,fbpage)


    filenamepostfix = filenamepostfix.rstrip('-')
    # Determine Stop Words for WordCloud
    stopwords = set(STOPWORDS)
    stopwords.update(["lot","less","https","anybody","actually","said","one", "many", "two", "people", "time", "according","called","used","proc","click","external","links","chew","says","that"])

    # Setup image mask and use colors from the mask
    masks = []
    maskName = []
    for file in glob.glob("images\\" + keywords + "*_Final*"):
        masks.append(file)
        maskName.append(os.path.splitext(os.path.basename(file))[0])

    for file in glob.glob("images\\" + keywords + "*_Transparent*"):
        masks.append(file)
        maskName.append(os.path.splitext(os.path.basename(file))[0])

    #masks = ['images\\' + keywords + '_Final.jpg','images\\' + keywords + '_Transparent.jpg']
    #maskName = ['Final','Transparent']

    # Loop all sets of words for different word clouds
    """words = ""
    filenamepostfix = ""
    if (len(twitter_string) > 0):
        words = twitter_string
        filenamepostfix = "Twitter"
    
    if (len(wiki_string) > 0):
        words = wiki_string
        filenamepostfix = "Wiki"
    
    if (len(file_string) > 0):
        words = file_string
        filenamepostfix = "File"

    if (len(newsapi_string) > 0):
        words = newsapi_string
        filenamepostfix = "NewsApi"
    
    if (len(nytimes_string) > 0):
        words = nytimes_string
        filenamepostfix = "NYTimes"
    
    if (len(reddit_string) > 0):
        words = reddit_string
        filenamepostfix = "Reddit"
        
    if (len(all_string) > 0):
        words = all_string
        filenamepostfix = "All"
    """
    #wordgroups = [twitter_string, wiki_string, all_string]
    #filenamepostfix = ["_Twitter", "_Wiki", "_All"]

    #words = words.replace("michaeljordanultimatefanpage", "michael jordan ultimate fan page")
    #words = words.replace("michaeljordan", "michael jordan")
    try:
        words = words.lower()
    except Exception as e:
        logging.info("Error with lower casing the words:" + str(e))
        pass

    #i = 0
    #for words in wordgroups:
    j = 0
    i = 0

    if len(masks) == 0:
        wordcloud = WordCloud(include_numbers=True, width=1600, mask=None,
                              stopwords=stopwords, height=800, max_font_size=200, max_words=1000, repeat=True,
                              collocations=True,
                              mode="RGBA", background_color="rgba(255, 255, 255, 0)", normalize_plurals=False).generate(
            words)

        wordcloud.to_file('output\\' + keywords + '_WordCloud_' + filenamepostfix + '_NoMask.png')
    else:
        for mask_path in masks:
            logging.info("Making File for mask:" + str(mask_path))
            if not exists(mask_path):
                if i == 0:
                    i += 1
                    wordcloud = WordCloud(include_numbers=True, width=1600, mask=None,
                                      stopwords=stopwords, height=800, max_font_size=200, max_words=1000, repeat=True,
                                      collocations=True,
                                      mode="RGBA", background_color="rgba(255, 255, 255, 0)", normalize_plurals=False).generate(words)

                    wordcloud.to_file('output\\' + keywords + '_WordCloud_' + filenamepostfix + '_' + maskName[j] + '.png')
                    """
                    # Make wordcloud art with no mask
                    f = plt.figure(figsize=(50, 50))
                    plt.plot(1, 1)
                    plt.imshow(wordcloud, interpolation='bilinear')
                    plt.axis("off")
                    plt.savefig('output\\' + keywords + 'NoMaskExists.png')
                    # plt.show()
                    """
            else:
                print("Generating Word Cloud from: " + filenamepostfix + " for mask: " + maskName[j])
                logging.info("Generating Word Cloud from: " + filenamepostfix + " for mask: " + maskName[j])
                image = Image.open(mask_path)
                mask = np.array(image)
                #mask = mask[::3, ::3]


                # create mask  white is "masked out"
                #image_mask = mask.copy()
                #image_mask[image_mask.sum(axis=2) == 0] = 255

                # some finesse: we enforce boundaries between colors so they get less washed out.
                # For that we do some edge detection in the image
                #edges = np.mean([gaussian_gradient_magnitude(mask[:, :, i] / 255., 2) for i in range(3)], axis=0)
                #image_mask[edges > .08] = 255

                image_colors = ImageColorGenerator(mask, default_color="rgba(255, 255, 255, 0)")

                if len(font) == 0:
                    #font = random.choice(os.listdir('\\fonts'))
                    font = random.choice(glob.glob("C:\\Windows\\Fonts\\*.ttf"))

                wordcloud = WordCloud(include_numbers=True, font_path=font, width=image.width, mask=mask,
                                      stopwords=stopwords, height=image.height, max_font_size=200, max_words=1000,repeat=True, collocations=True,
                                      mode="RGBA", background_color="rgba(255, 255, 255, 0)", normalize_plurals=False).generate(words)

                if usecolor.__contains__('y'):
                    wordcloud.recolor(color_func=image_colors)

                wordcloud.to_file('output\\' + keywords + '_WordCloud_' + filenamepostfix + '_' + maskName[j] + '.png')

                """
                # Make wordcloud art showing both Words and Mask
                f = plt.figure(figsize=(50, 50))
                f.add_subplot(1, 2, 1)
                plt.imshow(mask, cmap=plt.cm.gray, interpolation='bilinear')
                plt.axis("off")
                f.add_subplot(1, 2, 2)
                plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation='bilinear')
                plt.axis("off")
                plt.savefig('output\\' + keywords + '_Both_' + filenamepostfix + '_' + maskName[j] + '.png')
    
                # Make wordcloud art showing Words with Mask
                f = plt.figure(figsize=(50, 50))
                plt.plot(1, 1)
                plt.imshow(mask, cmap=plt.cm.gray, interpolation='bilinear')
                plt.plot(1, 1)
                plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation='bilinear')
                plt.axis("off")
                plt.savefig('output\\' + keywords + '_WithMask_' + filenamepostfix + '_' + maskName[j] + '.png')
                # plt.show()
                """
                """
                ##########################################################
                # Make wordcloud art showing just Words and no Mask
                f = plt.figure(figsize=(50, 50))
                plt.plot(1, 1)
                #if usecolor.__contains__('y'):
                #    plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation='bilinear')
                #
                #else:
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis("off")
                plt.savefig('output\\' + keywords + '_NoMask_' + filenamepostfix + '_' + maskName[j] + '.png')
                # plt.show()
                ##########################################################
                """
                """
                f = plt.figure(figsize=(50, 50))
                plt.plot(1, 1)
                im = plt.imshow(wordcloud.recolor(color_func=image_colors), animated=True, interpolation='bilinear')
        
                def update(i):
                    A = np.random.randn(10, 10)
                    im.set_array(A)
                    return im
        
                # plt.title('Art', size=80)
                plt.axis("off")
                plt.savefig('output\\' + keywords + '_NoMask' + filenamepostfix[i] + '_' + maskName[j] + '.png')
        
                ani = FuncAnimation(plt.gcf(), update, frames=range(100), interval=5, blit=False)
                ani.save('output\\' + keywords + '_Animated' + filenamepostfix[i] + '_' + maskName[j] + '.gif', writer = 'imagemagick')
        
                plt.show()
                """
                j += 1

    try:
        os.remove("./#" + keywords + "-filter")
    except Exception as e:
        logging.info("Error with Removing Twitter CSV:" + str(e))
        pass

    print("Done")
    logging.info("Done")

if __name__ == "__main__":
    main(sys.argv[1:])

