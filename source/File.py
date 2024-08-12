# importing the module

#keywords = sys.argv[1]
keywords = "KobeBryant"
file = "data\\KobeBryant.txt"

# Download Picture

# Remove Background
f = open(file,"r",encoding='utf-8')
lines = f.readlines()

text = ""

for line in lines:
    text += line

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt


stopwords = set(STOPWORDS)
stopwords.update(["elonmusk","elon musk","elon","musk","spacex"])

import numpy as np
from PIL import Image


# In[288]:


mask = np.array(Image.open('images\\' + keywords + '_Final.jpg'))
image_colors = ImageColorGenerator(mask)

wordcloud = WordCloud(include_numbers=True,font_path="fonts\\AnyConv.com__Lakers-Regular 400.ttf", width=1600,mask=mask,stopwords=stopwords,height=800,max_font_size=200,max_words=1000,collocations=True,mode = "RGBA", background_color=None).generate(text)


f = plt.figure(figsize=(50,50))
plt.plot(1,1)
plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation='bilinear')
plt.axis("off")
plt.savefig('output\\' + keywords + 'Quotes.png')

