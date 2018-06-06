from tweepy import OAuthHandler
from tweepy import API
import json
from time import sleep

# keys and tokens removed
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth)

# opens our JSON file
json_input = open('tweets.json')

# loads our JSON file
data = json.load(json_input)

# selects the specific node from the JSON
tweets = data["tweets"]

for tweet in tweets:
    api.update_status(tweet)
    sleep(1800)