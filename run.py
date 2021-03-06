__author__ = 'Tomasz Warkocki'

from constants import *
from data_collector import DataCollector
from data_preprocessor import DataPreprocessor
from experiment import Experiment

data_collector = DataCollector('data/tweets', POSITIVE_EMOTICONS + NEGATIVE_EMOTICONS, 30000)
data_collector.execute()

preprocessor = DataPreprocessor('data/tweets')
preprocessor.execute()

preprocessor = Experiment('data/ready_tweets')
preprocessor.execute()