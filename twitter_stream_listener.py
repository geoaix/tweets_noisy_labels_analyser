__author__ = 'Tomasz Warkocki'

from tweepy.streaming import StreamListener
from json import loads, dumps


class TwitterStreamListener(StreamListener):
    def __init__(self, file_path, limit=100):
        super(StreamListener, self).__init__()
        self.tweets_count = 0
        self.limit = limit
        self.file_path = file_path

    def on_data(self, raw_data):
        try:
            tweet = loads(raw_data)
            tweet_text = tweet['text']

            with open(self.file_path, 'a') as df:
                df.write(dumps(tweet_text.encode('utf8')) + '\n')
                self.tweets_count += 1
                print self.tweets_count

            if self.should_stop():
                return False

        except Exception, e:
            print 'Error', e

    def on_error(self, status):
        print status

    def should_stop(self):
        return self.tweets_count == self.limit