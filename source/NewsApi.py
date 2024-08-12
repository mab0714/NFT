import sys
from newsapi import NewsApiClient
from newspaper import Article
import re
import math

keywords = sys.argv[1]

def getPage(keywords, page, text,f,newsapi):
    all_articles = newsapi.get_everything(
        q=keywords,
        language='en',
        page=page
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
            data += "\n" + text +"\n"+ summary + "\n" + ' '.join(keywords) + "\n" + title
            f.write(data + "\n")
        except Exception as e:
            continue
    return numPages, text


def clean_text(text):
    '''
    Utility function to clean text by removing links, special characters
    using simple regex statements.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())

def getNewsApi(keywords):
    newsapi = NewsApiClient(api_key='28c66e5fc20e435298767d2a4a899e03')

    f = open("C:\\Users\\Marvin\\Desktop\\NFT\\source\\data\\newsapi_" + keywords + ".txt", "a", encoding="utf8")

    numPages, text = getPage(keywords,1,"",f, newsapi)
    newsapi_string = text
    for page in range(numPages):
        if page > 1:
            try:
                numPages, text = getPage(keywords, page, text,f,newsapi)
                newsapi_string += "\n" + text
            except Exception as e:
                continue
    f.close()
    return newsapi_string


newsapi_string = getNewsApi(keywords)