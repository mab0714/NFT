import sys

from imdb import Cinemagoer
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

keywords = sys.argv[1]

stopwords = set(STOPWORDS)
stopwords.update(["elonmusk","elon musk","elon","musk","spacex"])

# create an instance of the Cinemagoer class
ia = Cinemagoer()
"""
movie_info = ia.get_movie_infoset()
filtered = filter(lambda item: item.__contains__('review') == True, ia.get_movie_infoset())

person_info = ia.get_person_infoset()

company_info = ia.get_company_infoset()
"""

def getMovieData(keywords):
    print("Getting Movie reviews: " + keywords)
    movie = ia.get_movie(keywords)

    filtered = filter(lambda item: item.__contains__('review') == True, ia.get_movie_infoset())
    f = open("C:\\Users\\Marvin\\Desktop\\NFT\\source\\data\\imdb_" + keywords + ".txt", "w", encoding="utf8")
    review_string = ""
    for review_type in filtered:
        ia.update(movie, [review_type])
        try:
            for review in movie[review_type]:
                if (review['rating'] > 8):
                    for helpful in range(review['helpful']):
                        f.write(review['content'] + "\n")
                        review_string += review['content']
        except:
            continue

    f.close()
    return review_string

def getMovieData2(keywords):
    print("Getting Movie reviews: " + keywords)
    reviews = ia.get_movie_reviews(keywords)
    review_string = ""
    f = open("C:\\Users\\Marvin\\Desktop\\NFT\\source\\data\\imdb_" + keywords + ".txt", "w", encoding="utf8")

    for review in reviews['data']['reviews']:
        try:
            if (review['rating'] > 8):
                for helpful in range(review['helpful']):
                    f.write(review['content'] + "\n")
                    review_string += review['content']
        except:
            continue

    f.close()
    return review_string

# get a movie reviews
review_string = getMovieData2(keywords)
#movie = ia.get_movie('0068646')

#filtered = filter(lambda item: item.__contains__('review') == True, ia.get_movie_infoset())


#for review_type in filtered:
#    ia.update(movie, [review_type])
#    try:
#        for review in movie[review_type]:
#            print(review)
#    except:
#        continue

# print the names of the directors of the movie
#print('Directors:')
#for director in movie['directors']:
#    print(director['name'])

# print the genres of the movie
#print('Genres:')
#for genre in movie['genres']:
#    print(genre)

# search for a person name
#people = ia.search_person('Mel Gibson')
#for person in people:
#   print(person.personID, person['name'])
