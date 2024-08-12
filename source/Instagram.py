"""
from instagramy import *

user = InstagramUser('instagram')
tag = InstagramHashTag('michaeljordan')
tag.tag_data
"""

# importing the modules
import instagram_explore as ie
import json

# using the tag method
result = ie.tag('michaeljordan')

parsed_data = json.dumps(result, indent = 4,sort_keys = True)

# displaying the data
print(parsed_data)


a= 5