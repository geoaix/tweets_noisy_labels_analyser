__author__ = 'Tomasz Warkocki'

from constants import *
import re
import os


class DataPreprocessor:
    def __init__(self, file_path):
        self.file_path = file_path

    def execute(self):
        self.remove_duplicates(self.file_path, 'data/unique_tweets')
        self.clear_unneeded_data('data/unique_tweets', 'data/preprocessed_tweets')
        self.label_tweets('data/preprocessed_tweets', 'data/ready_tweets', 5000)
        os.remove('data/unique_tweets')
        os.remove('data/preprocessed_tweets')

    def remove_duplicates(self, in_file_path, out_file_path):
        seen_lines = set()
        outfile = open(out_file_path, "w")
        for line in open(in_file_path, "r"):
            if line not in seen_lines:
                outfile.write(line)
                seen_lines.add(line)
        outfile.close()

    def clear_unneeded_data(self, in_file_path, out_file_path):
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        username_pattern = r'@\w+:*'
        unicode_emojis_pattern = r'\\u....'
        outfile = open(out_file_path, "w")
        for line in open(in_file_path, "r"):
            cleaned_line = re.sub(url_pattern, 'URL', line)
            cleaned_line = re.sub(username_pattern, '', cleaned_line)
            cleaned_line = re.sub(r'\\n', '', cleaned_line)
            cleaned_line = re.sub(r'RT', '', cleaned_line)
            cleaned_line = re.sub(unicode_emojis_pattern, '', cleaned_line)
            cleaned_line = re.sub(r'"', '', cleaned_line)
            cleaned_line = re.sub(r';', '', cleaned_line)
            outfile.write(cleaned_line.strip() + '\n')


    def label_tweets(self, in_file_path, output_file_path, limit):
        positive_count = 0
        negative_count = 0
        output_file = open(output_file_path, "w")
        for tweet in open(in_file_path, "r"):
            positive = self.include_emojis(tweet, POSITIVE_EMOTICONS)
            negative = self.include_emojis(tweet, NEGATIVE_EMOTICONS)
            if negative != positive:
                tweet = self.remove_emojis(tweet, POSITIVE_EMOTICONS + NEGATIVE_EMOTICONS)
                if positive and positive_count < limit:
                    self.write_tweet_to_file(output_file, tweet, 1)
                    positive_count += 1
                if negative and negative_count < limit:
                    self.write_tweet_to_file(output_file, tweet, 0)
                    negative_count += 1


    def include_emojis(self, tweet, emojis):
        for emoji in emojis:
            if tweet.find(emoji) >= 0:
                return True
        return False

    def remove_emojis(self, tweet, emojis):
        for emoji in emojis:
            tweet = tweet.replace(emoji, '')
        return tweet

    def write_tweet_to_file(self, file, tweet, polarity):
        file.write(str(polarity) + ';' + tweet)