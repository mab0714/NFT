# importing the module
import wikipedia
import pandas as pd
from datetime import time
import sys

from matplotlib.animation import FuncAnimation

keywords = sys.argv[1]
#keywords = "JohnnyDepp"

# Download Picture

# Remove Background
#https://dashboard.photoroom.com/accounts/login/

# Convert PNG to JPEG
#https://www.geeksforgeeks.org/convert-png-to-jpg-using-python/

# wikipedia page object is created

results = wikipedia.search(keywords, results = 5)

page_objects = []
for result in results:
    try:
        page_objects.append(wikipedia.page(result))
    except Exception as e:
        continue


from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt


stopwords = set(STOPWORDS)
stopwords.update(["elonmusk","elon musk","elon","musk","spacex"])

import numpy as np
from PIL import Image


# In[288]:


mask = np.array(Image.open('images\\' + keywords + '_Final.jpg'))
image_colors = ImageColorGenerator(mask)

text = ""
for object in page_objects:
    text += object.content

wordcloud = WordCloud(include_numbers=True,font_path="fonts\\ParmaPetit-HeavySwinging.ttf", width=1600,mask=mask,stopwords=stopwords,height=800,max_font_size=200,max_words=1000,collocations=True,mode = "RGBA", background_color=None).generate(text)


f = plt.figure(figsize=(50,50))
f.add_subplot(1,2, 1)
plt.imshow(mask, cmap=plt.cm.gray, interpolation='bilinear')
plt.axis("off")
f.add_subplot(1,2, 2)
plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation='bilinear')
plt.axis("off")
plt.savefig('output\\' + keywords + 'BothWiki.png')


#wordcloud = WordCloud(include_numbers=True,font_path="fonts\\NBA Cavaliers.ttf",width=1600,mask=mask,stopwords=stopwords,height=800,max_font_size=200,max_words=1000,collocations=True,mode = "RGBA", background_color=None).generate(string)
f = plt.figure(figsize=(50,50))
plt.plot(1,1)
plt.imshow(mask, cmap=plt.cm.gray, interpolation='bilinear')
plt.plot(1,1)
plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation='bilinear')
#plt.title('Art', size=80)
plt.axis("off")
plt.savefig('output\\' + keywords + 'WithMaskWiki.png')
#plt.show()

f = plt.figure(figsize=(50,50))
plt.plot(1,1)
plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation='bilinear')
#plt.title('Art', size=80)
plt.axis("off")
plt.savefig('output\\' + keywords + 'NoMaskWiki.png')
#plt.show()

"""
f = plt.figure(figsize=(50, 50))
plt.plot(1, 1)
im = plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation='bilinear')

def update(i):
    a = im.get_array()
    a = a * np.exp(-0.001 * i)  # exponential decay of the values
    im.set_array(a)
    return [im]

# plt.title('Art', size=80)
plt.axis("off")
#plt.savefig('output\\' + keywords + 'NoMask.png')

ani = FuncAnimation(f, update, frames=range(100), interval=100, blit=False)
ani.save('output\\' + keywords + '_Animated.gif')
###
#plt.show()
"""