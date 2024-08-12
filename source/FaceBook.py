"""
WORKED, but locks account
from facebook_scraper import get_posts

f = open("C:\\Users\\Marvin\\Desktop\\NFT\\source\\data\\tristanpeigne3.txt", "w", encoding="utf8")


for post in get_posts('tpeigne',credentials=('mab0714@yahoo.com',''),pages=1000):
    if post['text'] is None:
        continue
    else:
        if ((post['username'] == 'Tristan Peigne')):
            likes = int(post['likes']) * 50
        else:
            likes = int(post['likes'])

        for reaction in range(likes):
            f.write(post['text'] + "\r\n")


f.close()
"""


import sys
from facebook_page_scraper import Facebook_scraper
import json

#instantiate the Facebook_scraper class

keywords = sys.argv[1]
recent = int(sys.argv[2])


def getFacebookData(keywords, recent):
    page_name = keywords
    posts_count = recent
    browser = "chrome"

    facebook_ai = Facebook_scraper(page_name, posts_count, browser)

    json_data = facebook_ai.scrap_to_json()
    data_dict = json.loads(json_data)

    f = open("C:\\Users\\Marvin\\Desktop\\NFT\\source\\data\\facebook_" + keywords.replace("+", "") + ".txt", "a",
             encoding="utf8")
    facebook_string = ""
    for key in data_dict:
        if (len(data_dict[key]['content']) > 0):
            try:
                f.write((max(data_dict[key]['reaction_count'], 1)) * (data_dict[key]['content']))
                facebook_string += (max(data_dict[key]['reaction_count'], 1)) * (data_dict[key]['content'])
            except Exception as e:
                f.write(data_dict[key]['content'])
                facebook_string += data_dict[key]['content']

    f.close()
    return facebook_string

facebook_string = getFacebookData(keywords,recent)


"""
#import Facebook_scraper class from facebook_page_scraper
from facebook_page_scraper import Facebook_scraper

#instantiate the Facebook_scraper class

page_name = "tpeigne"
posts_count = 10000
browser = "chrome"
proxy = "mab0714@yahoo.com:M@b040913@IP:PORT" #if proxy requires authentication then user:password@IP:PORT
timeout = 600 #600 seconds
meta_ai = Facebook_scraper(page_name,posts_count,browser,proxy=proxy,timeout=timeout)

json_data = meta_ai.scrap_to_json()
print(json_data)

filename = "tristanpeigne2"  #file name without CSV extension,where data will be saved
directory = "C:\\Users\\Marvin\\Desktop\\NFT\\source\\data" #directory where CSV file will be saved
meta_ai.scrap_to_csv(filename,directory)

"""


import csv
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
"""
f = open("C:\\Users\\Marvin\\Desktop\\NFT\\source\\data\\tristanpeigne.txt", "w", encoding="utf8")


# opening the CSV file
with open('C:\\Users\\Marvin\\Desktop\\NFT\\source\\data\\tristanpeigne.csv', mode='r', encoding="utf8") as file:
    # reading the CSV file
    csvFile = csv.reader(file)

    # displaying the contents of the CSV file
    i = 0
    for lines in csvFile:
        if len(lines[12]) > 0:
            if (i > 0):
                for reaction in range(int(lines[10])):
                    f.write(lines[12] + "\r\n")
        i += 1

f.close()
"""

def getFileData(keywords):
    print("Getting File data for: " + keywords)
    file = "data\\" + keywords + ".txt"
    f = open(file, "r", encoding='utf-8')
    lines = f.readlines()

    file_string = ""

    for line in lines:
        file_string += line

    return file_string


file_string = getFileData('tristanpeigne')

stopwords = set(STOPWORDS)
stopwords.update(["see", "many", "will", "made", "trying", "way","always"])
wordcloud = WordCloud(include_numbers=True,font_path="fonts\\NBA Bulls.ttf", width=1600,stopwords=stopwords,height=800,min_word_length=4,repeat=True,scale=1,max_font_size=200,max_words=1000,collocations=True,mode = "RGBA", background_color=None).generate(file_string)

# display wordcloud
wordcloud = WordCloud(width=1600, stopwords=stopwords,height=800,max_font_size=200,max_words=50,collocations=False, background_color='grey').generate(file_string)
plt.figure(figsize=(40,30))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
