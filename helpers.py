# coding=utf8
from pymongo import MongoClient
from config import *
import math

client = MongoClient()
db = client[DB_NAME]
col = db[COL_NAME]


def get_posts_by_page_and_category(page, category):
    data = get_data_by_category(category)
    return list(data.skip((page - 1) * NUM_PER_PAGE).limit(NUM_PER_PAGE))


def get_pages_num(page, category):
    data = get_data_by_category(category)
    total_page = int(math.ceil(data.count()/float(NUM_PER_PAGE)))
    if page + NUM_PER_PAGE > total_page:
        if total_page > NUM_PER_PAGE:
            start_page = total_page - NUM_PER_PAGE + 1
        else:
            start_page = 1
        end_page = total_page + 1
    else:
        start_page = page
        end_page = page + NUM_PER_PAGE
    return start_page, end_page,  total_page


def get_data_by_category(category):
    if category == "all":
        posts = col.find({})
    elif category == "visit":
        posts = col.find({'visit': True})
    else:
        posts = col.find({'read': False})
    return posts
