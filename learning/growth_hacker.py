# coding=utf8
from __future__ import absolute_import
from pymongo import MongoClient
import jieba
import re


client = MongoClient()
db = client['ai']
gh_col = db['gh']

my_list_c = db["mylist"]


def handle_word(word):
    word = word.lower().strip()
    p = re.compile('[a-z]+')
    if not p.match(word):
        return None
    if len(word) < 2:
        return None
    return word


def make_keywords():
    items = gh_col.find({})
    result = {}
    for i in items:
        words = jieba.cut(i['title'])
        for w in words:
            word = handle_word(w)
            if not word:
                continue
            result.setdefault(word, 0)
            result[word] += 1
    my_list = []
    for k, v in result.iteritems():
        if v > 5:
            my_list.append(k)
    my_list_c.insert({'gh': my_list})


if __name__ == "__main__":
    make_keywords()
