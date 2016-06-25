# coding=utf8

from flask import Flask, render_template, request
from pymongo import MongoClient
from bson.json_util import dumps
import math
from config import *


app = Flask(__name__)
client = MongoClient()
db = client[DB_NAME]
col = db[COL_NAME]


@app.route("/")
def growth_hackers():
    return render_template("growth_hackers.html")


@app.route("/posts")
def get_posts():
    try:
        page = int(request.args.get('page', 1))
    except Exception as e:
        page = 1
    total_page = int(math.ceil(col.count()/float(NUM_PER_PAGE)))
    if page + NUM_PER_PAGE > total_page:
        if total_page > NUM_PER_PAGE:
            start_page = total_page - NUM_PER_PAGE + 1
        else:
            start_page = 1
        end_page = total_page + 1
    else:
        start_page = page
        end_page = page + NUM_PER_PAGE
    return dumps({
        "total": total_page,
        "cur_page": page,
        "page_list": range(start_page, end_page),
        "posts": col.find().skip((page-1) * NUM_PER_PAGE).limit(NUM_PER_PAGE)
    })
