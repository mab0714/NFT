import sys
from newspaper import Article
from nytimesarticle import articleAPI
import requests
import json
import re

# https://developer.nytimes.com/apis
keywords = sys.argv[1]

def clean_text(text):
    '''
    Utility function to clean text by removing links, special characters
    using simple regex statements.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())


def getNYTimes(keywords):
    api = articleAPI("ahIYn6AjQ1iQMIkrYGI7GGIaL1jkyCw8")
    r = requests.get('https://api.nytimes.com/svc/search/v2/articlesearch.json?query='+keywords+'&api-key=ahIYn6AjQ1iQMIkrYGI7GGIaL1jkyCw8')
    datastore = json.loads(r.text)

    f = open("C:\\Users\\Marvin\\Desktop\\NFT\\source\\data\\nyt_" + keywords + ".txt", "a", encoding="utf8")
    data = ""
    for doc in datastore['results']:
        web_url = doc['link']['url']
        try:
            article = Article(web_url)
            article.download()
            article.parse()
            article.nlp()
            title = article.title
            text = clean_text(article.text)
            keywords = article.keywords
            summary = clean_text(article.summary)
            data += "\n" + text +"\n"+ summary + "\n"+ keywords + "\n" + title
            f.write(data + "\n")

        except:
            continue

    return data
    f.close()

nytimes_string = getNYTimes(keywords)
