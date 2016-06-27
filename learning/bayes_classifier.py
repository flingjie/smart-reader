# coding=utf8

from helpers import gh_col
from pandas import DataFrame
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer


def build_data_frame(items):
    rows = []
    for i in items:
        rows.append({'text': i['title'], 'class': i['visit']})

    data_frame = DataFrame(rows)
    return data_frame


def get_pipeline():
    items = gh_col.find({})
    data = build_data_frame(items)

    text_clf = Pipeline([('vect', CountVectorizer()),
                        ('tfidf', TfidfTransformer()),
                        ('clf', MultinomialNB()),
                       ])

    text_clf.fit(data['text'].values, data['class'].values)
    return text_clf


def bayes_classifier():
    pipeline = get_pipeline()

    result = pipeline.predict()
    return result
