# 参考doc/controller/buyer文档，处理前端请求
# 实现基于be/service/buyer提供的接口
from flask import Blueprint
from flask import request
from flask import jsonify
from be.service import buyer
import json

bp_buyer = Blueprint("buyer", __name__, url_prefix="/buyer")


@bp_buyer.route("/new_order", methods=["POST"])
def new_order():
    try:
        data = request.get_data()
        mydict = json.loads(data)
        buyer_id = mydict['user_id']
        store_id = mydict['store_id']
        books_dict = mydict['books']
        books = [(book['id'], book['count']) for book in books_dict]
    except:
        return jsonify({"message": "Missing form data."}), 518

    token = request.headers.get("token")

    code, msg, order_id = buyer.new_order(buyer_id, store_id, books, token)
    return jsonify({"message": msg, "order_id": order_id}), code

@bp_buyer.route("/cancel", methods=["POST"])
def cancel():
    try:
        data = request.get_data()
        mydict = json.loads(data)
        buyer_id = mydict['user_id']
        order_id = mydict['order_id']
    except:
        return jsonify({"message": "Missing form data."}), 518

    token = request.headers.get("token")

    code, msg = buyer.manual_cancel(token, buyer_id, order_id)

    return jsonify({"message": msg}), code


@bp_buyer.route("/payment", methods=["POST"])
def payment():
    try:
        data = request.get_data()
        mydict = json.loads(data)
        buyer_id = mydict['user_id']
        order_id = mydict['order_id']
        password = mydict['password']
    except:
        return jsonify({"message": "Missing form data."}), 518

    code, msg = buyer.payment(buyer_id, order_id, password)
    return jsonify({"message": msg}), code

@bp_buyer.route("/add_funds", methods=["POST"])
def add_funds():
    try:
        data = request.get_data()
        mydict = json.loads(data)
        buyer_id = mydict['user_id']
        password = mydict['password']
        add_value = int(mydict['add_value'])
    except:
        return jsonify({"message": "Missing form data."}), 518

    code, msg = buyer.add_funds(buyer_id, password, add_value)
    return jsonify({"message": msg}), code

@bp_buyer.route("/delivery_confirmed", methods=["POST"])
def delivery_confirmed():
    try:
        data = request.get_data()
        mydict = json.loads(data)
        buyer_id = mydict['user_id']
        order_id = mydict['order_id']
    except:
        return jsonify({"message": "Missing form data."}), 518

    code, msg = buyer.delivery_confirmed(buyer_id, order_id)

    return jsonify({"message": msg}), code

@bp_buyer.route("/search_book", methods=["POST"])
def search_book():
    try:
        data = request.get_data()
        mydict = json.loads(data)
        keywords = mydict['keywords']
        params = mydict['params']
        is_title = params["is_title"]
        is_content = params["is_content"]
        is_author = params["is_author"]
        is_tag = params["is_tag"]
    except:
        return jsonify({"message": "Missing form data."}), 518

    code, msg, book_list = buyer.search_book(keywords,is_title,is_content,is_author,is_tag)

    return jsonify({"message": msg, "book_list": book_list}), code

@bp_buyer.route("/comment", methods=["POST"])
def comment():
    try:
        data = request.get_data()
        mydict = json.loads(data)
        buyer_id = mydict['buyer_id']
        order_id = mydict['order_id']
        score = mydict['score']
        comment = mydict['comment']
    except:
        return jsonify({"message": "Missing form data."}), 518
    
    token = request.headers.get("token")

    code, msg = buyer.comment(token, buyer_id, order_id, score, comment)

    return jsonify({"message": msg}), code


@bp_buyer.route("/search_comment", methods=["POST"])
def search_comment():
    try:
        data = request.get_data()
        mydict = json.loads(data)
        store_id = mydict['store_id']
    except:
        return jsonify({"message": "Missing form data."}), 518, None

    code, msg, comment_list = buyer.search_comment(store_id)

    return jsonify({"message": msg, "comment_list": comment_list}), code


@bp_buyer.route("/check_order_status", methods=["POST"])
def check_order_status():
    try:
        data = request.get_data()
        mydict = json.loads(data)
        buyer_id = mydict['buyer_id']
        order_id = mydict['order_id']

    except:
        return jsonify({"message": "Missing form data."}), 518

    token = request.headers.get("token")

    code, msg, status = buyer.check_order_status(token, buyer_id, order_id)

    return jsonify({"message": msg, "status": status}), code


@bp_buyer.route("/check_order_history_ongoing", methods=["POST"])
def check_order_history_ongoing():
    try:
        data = request.get_data()
        mydict = json.loads(data)
        buyer_id = mydict['buyer_id']

    except:
        return jsonify({"message": "Missing form data."}), 518

    token = request.headers.get("token")

    code, msg, ongoing_order = buyer.check_order_history_ongoing(token, buyer_id)

    return jsonify({"message": msg, "ongoing_order": ongoing_order}), code


@bp_buyer.route("/check_order_history", methods=["POST"])
def check_order_history():
    try:
        data = request.get_data()
        mydict = json.loads(data)
        buyer_id = mydict['buyer_id']

    except:
        return jsonify({"message": "Missing form data."}), 518

    token = request.headers.get("token")

    code, msg, history_order = buyer.check_order_history(token, buyer_id)

    return jsonify({"message": msg, "history_order": history_order}), code