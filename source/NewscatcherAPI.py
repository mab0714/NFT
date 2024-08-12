import sys
from newscatcherapi import NewsCatcherApiClient

keywords = sys.argv[1]
# https://newscatcherapi.com/news-api

newscatcherapi = NewsCatcherApiClient(x_api_key='YOUR_API_KEY')

all_articles = newscatcherapi.get_search_all_pages(q=keywords,
                                         lang='en',
                                         countries='US',
                                         page_size=100,
                                         max_page=10,
                                         seconds_pause=1.0
                                         )