#!/usr/bin/env python
# coding: utf-8

# In[292]:


# This notebook is about making wordcloud of tweets using python


# In[ ]:
import os
import sys
from datetime import time

import tweepy
import pandas as pd
import re

import DuckDuckGoImages as ddg

import emoji
import nltk
import preprocessor as p

# In[14]:
keywords = sys.argv[1]


access_token = "4192621779-R2yag5NcDn0aisOAAPmhEoaMfneL39hJSneU1ev"
access_token_secret = "LKgkU8tNxs45gLiHN6zPOU57VXp6338tdvCxb6tZc6gkw"
consumer_key = "kk32njRRde69Jqtq4l2e7dOT3"
consumer_secret = "IQtaWbqdNXPgVNCEqdbn9x1fjKyMX0mLulEzK1BYkaM4F9OVJB"


# In[15]:


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


# In[16]:


def keyword_to_csv(keyword,recent): 
    try:
        tweets = tweepy.Cursor(api.search,q=keyword).items(recent)
        tweets_list = [[tweet.text] for tweet in tweets]
        df = pd.DataFrame(tweets_list,columns=['Text'])
        df.to_csv('{}.csv'.format(keyword), sep=',', index = False)
    except BaseException as e:
        print('failed on_status,',str(e))
        time.sleep(3)


# In[17]:


keyword = '#' + keywords + "-filter:retweets"
recent  = 3000
keyword_to_csv(keyword, recent)


# In[26]:


df = pd.read_csv("./#" + keywords + "-filter:retweets.csv")
pd.options.display.max_colwidth = 200
df.head()


# In[278]:


df.shape


# In[279]:


re_list = ['(https?://)?(www\.)?(\w+\.)?(\w+)(\.\w+)(/.+)?', '@[A-Za-z0-9_]+','#']
combined_re = re.compile( '|'.join( re_list) )


# In[280]:


regex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)


# In[281]:


from bs4 import BeautifulSoup
from nltk.tokenize import WordPunctTokenizer
token = WordPunctTokenizer()


# In[282]:


def cleaning_tweets(t):
    try:
        del_amp = BeautifulSoup(t, 'lxml')
        del_amp_text = del_amp.get_text()
        del_link_mentions = re.sub(combined_re, '', del_amp_text)
        del_emoticons = re.sub(regex_pattern, '', del_link_mentions)
        lower_case = del_emoticons.lower()
        words = token.tokenize(lower_case)
        result_words = [x for x in words if len(x) > 2]
        return (" ".join(result_words)).strip()
    except:
        return " "

# In[283]:



print("Cleaning the tweets...\n")
cleaned_tweets = []
for i in range(0,3000):
    if( (i+1)%100 == 0 ):
        print("Tweets {} of {} have been processed".format(i+1,3000))                                                                  
    try:
        cleaned_tweets.append(cleaning_tweets((df.Text[i])))
    except:
        continue


# In[284]:


string = pd.Series(cleaned_tweets).str.cat(sep=' ')


# In[285]:


from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

stopwords = set(STOPWORDS)
stopwords.update(["elonmusk","elon musk","elon","musk","spacex"])


# In[301]:


#wordcloud = WAIPordCloud(width=1600, stopwords=stopwords,height=800,max_font_size=200,max_words=50,collocations=False, background_color='grey').generate(string)
#plt.figure(figsize=(40,30))
#plt.imshow(wordcloud, interpolation="bilinear")
#plt.axis("off")
#plt.show()


# In[287]:


import numpy as np
from PIL import Image


# In[288]:


mask = np.array(Image.open('images\\' + keywords + '.jpg'))
image_colors = ImageColorGenerator(mask)

# In[297]:


wordcloud = WordCloud(include_numbers=True,font_path="fonts\\NBA Bulls.ttf", width=1600,mask=mask,stopwords=stopwords,height=800,max_font_size=200,max_words=1000,collocations=True,mode = "RGBA", background_color=None).generate(string)


# In[290]:


f = plt.figure(figsize=(50,50))
f.add_subplot(1,2, 1)
plt.imshow(mask, cmap=plt.cm.gray, interpolation='bilinear')
plt.axis("off")
f.add_subplot(1,2, 2)
plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation='bilinear')
plt.axis("off")
plt.savefig('output\\' + keywords + 'BothTwitter.png')


#wordcloud = WordCloud(include_numbers=True,font_path="fonts\\NBA Cavaliers.ttf",width=1600,mask=mask,stopwords=stopwords,height=800,max_font_size=200,max_words=1000,collocations=True,mode = "RGBA", background_color=None).generate(string)
f = plt.figure(figsize=(50,50))
plt.plot(1,1)
plt.imshow(mask, cmap=plt.cm.gray, interpolation='bilinear')
plt.plot(1,1)
plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation='bilinear')
#plt.title('Art', size=80)
plt.axis("off")
plt.savefig('output\\' + keywords + 'WithMaskTwitter.png')
#plt.show()

f = plt.figure(figsize=(50,50))
plt.plot(1,1)
plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation='bilinear')
#plt.title('Art', size=80)
plt.axis("off")
plt.savefig('output\\' + keywords + 'NoMaskTwitter.png')
#plt.show()

os.remove("./#" + keywords + "-filter")