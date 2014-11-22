__author__ = 'Tomasz Warkocki'

from tweepy import OAuthHandler
from tweepy import Stream
from twitter_stream_listener import TwitterStreamListener
from constants import *


class DataCollector:
    def __init__(self, file_path, filter_data, limit):
        self.file_path = file_path
        self.filter_data = filter_data
        self.limit = limit

    def execute(self):
        auth = OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        twitter_stream = Stream(auth, TwitterStreamListener(self.file_path, self.limit))
        twitter_stream.filter(track=self.filter_data, languages=['en'])