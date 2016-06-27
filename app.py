# coding=utf8
from bson.json_util import dumps
from flask import Flask, render_template, request
from bson.objectid import ObjectId
from helpers import get_posts_by_page_and_category, get_pages_num, gh_col
from config import OK

app = Flask(__name__)


@app.route("/")
def growth_hackers():
    return render_template("growth_hackers.html")


@app.route("/posts", methods=["POST"])
def get_posts():
    try:
        page = int(request.get_json()['page'])
        category = request.get_json()['category']
    except Exception as e:
        page = 1
        category = 'new'
    start_page, end_page, total_page = get_pages_num(page, category)
    posts = get_posts_by_page_and_category(page, category)
    return dumps({
        "total_page": total_page,
        "cur_page": page,
        "page_list": range(start_page, end_page),
        "posts": posts
    })


@app.route("/mark_all_read", methods=["POST"])
def mark_all_read():
    try:
        page = int(request.get_json()['page'])
        category = request.get_json()['category']
        ids = [ObjectId(i) for i in request.get_json()['ids']]
    except Exception as e:
        page = 1
        category = 'new'
    gh_col.update_many({"_id": {"$in": ids}}, {
        "$set": {
            "read": True
        },

    })
    start_page, end_page, total_page = get_pages_num(page, category)
    posts = get_posts_by_page_and_category(page, category)
    return dumps({
        "total_page": total_page,
        "cur_page": page,
        "page_list": range(start_page, end_page),
        "posts": posts
    })


@app.route("/mark_visit", methods=["POST"])
def mark_visit():
    obj_id = request.get_json()['obj_id']
    gh_col.update_one({"_id": ObjectId(obj_id)}, {
        "$set": {
            "visit": True
        },
    })
    return OK
