import tweepy
from datetime import date
from pprint import pprint
import re
import json

import os

user_id = "TheOmniLiberal"

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
recent_id = os.path.join(THIS_FOLDER, 'id.txt')

API_KEY = "lE87TYHKbfaLOZ0vaCnDv5hxd"
API_SECRET_KEY = "68zoEjoZwpO584YkBZLJSHIBJQOidksT34ctQHx8AMehRrF01X"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAACIZRgEAAAAAQMnhIa%2Bx1qYtS9u5qRDBiqi%2B%2F6U%3DJNxdDVlKOuzOYxEcCuo9GCxeXfegaSw4TfpMTqmZS5GwrRtzg9"

ACCESS_TOKEN = "1413748062812401666-vhBq7UaaYDvIyzbg6jhzQhVSzVKoh4"
ACCESS_TOKEN_SECRET = "SDrzTiZJbSxBMVKT9n2dojHifNpCykTsJ64nTOYBWy4NX"

auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

most_recent_id = None

with open(recent_id, "r") as fin:
    most_recent_id = fin.read()
    fin.close()

rec_id = None
if most_recent_id != "":
    rec_id = int(most_recent_id)

for status in api.user_timeline(id=user_id, since_id=rec_id, tweet_mode="extended"):
    if status.in_reply_to_status_id is None:
        print(status.full_text)
        tweet = re.sub("https://t\.co/[A-z0-9]+", "", status.full_text).strip()
        if tweet != '':
            api.update_status(tweet)

    else:
        print(status.full_text)
        tweet = re.sub("https://t\.co/[A-z0-9]+", "", status.full_text).strip()
        if tweet != "":
            temp1 = tweet.split(" ")
            temp2 = []
            flag = True

            while len(temp1) != 0:

                if len(temp1) > 0 and temp1[0][0] == '@' and flag:
                    temp1.pop(0)
                else:
                    flag = False
                    temp2.append(temp1.pop(0))
            tweet = " ".join(temp2)
            
            new_tweet = api.update_status(tweet)

            reply_text = "Replied to: https://twitter.com/twitter/statuses/" + str(api.get_status(status.in_reply_to_status_id).id)
            api.update_status(reply_text, in_reply_to_status_id=new_tweet.id)

cur_id = (api.user_timeline(id=user_id, count=1)[0]).id
with open(recent_id, "w") as fout:
    fout.write(str(cur_id))
    fout.close()
    
        
        
