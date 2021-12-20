# 参考doc/controller/seller文档，处理前端请求
# 实现基于be/service/seller提供的接口
from flask import Blueprint
from flask import request
from flask import jsonify
from be.service import seller
import json

bp_seller = Blueprint("seller", __name__, url_prefix="/seller")


@bp_seller.route("/create_store", methods=["POST"])
def create_store():
    try:
        data = request.get_data()
        mydict = json.loads(data)
        seller_id = mydict['user_id']
        store_id = mydict['store_id']
    except:
        return jsonify({"message": "Missing form data."}), 518
    
    token = request.headers.get("token")
    
    code, msg = seller.create_store(token, seller_id, store_id)
    return jsonify({"message": msg}), code

@bp_seller.route("/add_book", methods=["POST"])
def add_book():
    try:
        data = request.get_data()
        mydict = json.loads(data)
        seller_id = mydict['user_id']
        store_id = mydict['store_id']
        book_info = mydict['book_info']
        stock_level = mydict['stock_level']
    except:
        return jsonify({"message": "Missing form data."}), 518

    token = request.headers.get("token")
    
    code, msg = seller.add_book(token, seller_id, store_id, book_info, stock_level)
    return jsonify({"message": msg}), code

@bp_seller.route("/add_stock_level", methods=["POST"])
def add_stock_level():
    try:
        data = request.get_data()
        mydict = json.loads(data)
        seller_id = mydict['user_id']
        store_id = mydict['store_id']
        book_id = mydict['book_id']
        add_stock_level = mydict['add_stock_level']
    except:
        return jsonify({"message": "Missing form data."}), 518

    token = request.headers.get("token")

    code, msg = seller.add_stock_level(token, seller_id, store_id, book_id, add_stock_level)
    return jsonify({"message": msg}), code

@bp_seller.route("/delivery", methods=["POST"])
def delivery():
    try:
        data = request.get_data()
        mydict = json.loads(data)
        seller_id = mydict['user_id']
        store_id = mydict['store_id']
        order_id = int(mydict['order_id'])
    except:
        return jsonify({"message": "Missing form data."}), 518

    token = request.headers.get("token")

    code, msg = seller.delivery(token, seller_id, store_id, order_id)
    return jsonify({"message": msg}), code