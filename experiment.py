__author__ = 'Tomasz Warkocki'

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.cross_validation import cross_val_score, KFold
import numpy as np


class Experiment:
    def __init__(self, file_path):
        self.file_path = file_path

    def execute(self):
        dataset = np.genfromtxt(self.file_path, dtype=str, delimiter=";")
        target = dataset[:, 0].astype(int)
        data = dataset[:, 1]

        for pipeline in self.pipelines():
            self.evaluate_cross_validation(pipeline, data, target, 10)

    def pipelines(self):
        unigrams_clf = Pipeline(
            [
                ('vect', TfidfVectorizer(ngram_range=(1, 1), stop_words='english')),
                ('clf', MultinomialNB())
            ]
        )

        bigrams_clf = Pipeline(
            [
                ('vect', TfidfVectorizer(ngram_range=(1, 2), stop_words='english')),
                ('clf', MultinomialNB())
            ]
        )
        return [unigrams_clf, bigrams_clf]


    def evaluate_cross_validation(self, pipeline, x, y, k):
        cross_validation = KFold(len(y), k, shuffle=True, random_state=0)
        scores = cross_val_score(pipeline, x, y, cv=cross_validation)
        print scores
        print ('Mean score: {0:.3f}').format(np.mean(scores))