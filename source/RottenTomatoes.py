"""from rotten_tomatoes_client import RottenTomatoesClient, TvBrowsingCategory
result = RottenTomatoesClient.search(term="Old School", limit=5)

# doesn't give movieid to search movie details to get reviews

#https://github.com/jaebradley/rotten_tomatoes_client/blob/master/README.md#search

result = RottenTomatoesClient.get_movie_details(movie_id=446064253)

result = RottenTomatoesClient.browse_tv_shows(category=TvBrowsingCategory.most_popular)
"""

import rtsimple as rt
rt.API_KEY = 'YOUR API KEY HERE'