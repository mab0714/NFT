import sys
from pyyoutube import Api
from youtubesearchpython import *

keywords = sys.argv[1]
recent = int(sys.argv[2])

def getYouTubeData(keywords,recent):
    api = Api(api_key="")
    r = api.search_by_keywords(q=keywords, search_type=["comments"], count=recent, limit=50)
    f = open("C:\\Users\\Marvin\\Desktop\\NFT\\source\\data\\youtube_" + keywords.replace("+","") + ".txt", "w", encoding="utf8")
    youtube_string = ""
    for item in r.items:
        video_id = item.id.videoId
        comments = Comments(video_id)
        while comments.hasMoreComments:
            for comment in comments.comments['result']:
                try:
                    youtube_string += (max(comment['replyCount'],1)) * (comment['content'])
                    f.write((max(comment['replyCount'],1)) * (comment['content']) + "\r\n")
                except Exception as e:
                    youtube_string += comment['content']
                    f.write(comment['content'] + "\r\n")
            comments.getNextComments()
    f.close()

    return youtube_string

youtube_string = getYouTubeData(keywords,recent)


