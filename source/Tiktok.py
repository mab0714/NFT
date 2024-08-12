from TikTokApi import TikTokApi

with TikTokApi() as api:
        for hashtag in api.search_for_hashtags("funny"):
                print(hashtag.name)


a = 5