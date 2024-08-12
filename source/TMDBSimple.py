import tmdbsimple as tmdb
from tmdbsimple import Movies
# https://pypi.org/project/tmdbsimple/

#can't create instance of movie to get review...update: tmdb.Movies(response['results'][0])
# cant get reviews
tmdb.API_KEY = '096987ff48972ed456df88dee1f7fa83'
tmdb.REQUESTS_TIMEOUT = 5  # seconds, for both connect and read
search = tmdb.Search()

movies = tmdb.Movies()
response = search.movie(query='The Bourne')
if response is None:
    pass