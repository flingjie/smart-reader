# coding=utf8
from pymongo import MongoClient
from config import NUM_PER_PAGE
from config import *
import math

client = MongoClient()
db = client[DB_NAME]
col = db[COL_NAME]


def get_posts_by_page(page):
    posts = list(col.find({'read': False}).skip((page - 1) * NUM_PER_PAGE).limit(NUM_PER_PAGE))
    col.find({'read': False}).skip((page - 1) * NUM_PER_PAGE).limit(NUM_PER_PAGE)
    return posts


def get_pages_num(page):
    total_page = int(math.ceil(col.find({'read': False}).count()/float(NUM_PER_PAGE)))
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