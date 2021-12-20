# 参考doc/controller/auth文档，处理前端请求
# 实现基于be/service/auth提供的接口
from flask import Blueprint
from flask import request
from flask import jsonify
import json
from flask import Blueprint, request

from be.service import auth
bp_auth = Blueprint("auth", __name__, url_prefix="/auth")


@bp_auth.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_data()
        mydict = json.loads(data)
        user_id = mydict['user_id']
        user_password = mydict['password']
    except:
        return jsonify({"message": "User ID and password is required."}), 518
    code, msg = auth.register(user_id, user_password)
    return jsonify({"message": msg}), code


@bp_auth.route("/unregister", methods=["POST"])
def unregister():
    try:
        data = request.get_data()
        mydict = json.loads(data)
        user_id = mydict['user_id']
        user_password = mydict['password']
    except:
        return jsonify({"message": "User ID is required."}), 518
    code, msg = auth.unregister(user_id, user_password)
    return jsonify({"message": msg}), code


@bp_auth.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_data()
        mydict = json.loads(data)
        user_id = mydict['user_id']
        user_password = mydict['password']
        terminal = mydict['terminal']
    except:
        return jsonify({"message": "User ID and password and terminal is required."}), 518
    code, msg, token = auth.login(user_id, user_password, terminal)
    return jsonify({"message": msg, "token": token}), code


@bp_auth.route("/password", methods=["POST"])
def change_password():
    try:
        data = request.get_data()
        mydict = json.loads(data)
        user_id = mydict['user_id']
        old_password = mydict['oldPassword']
        new_password = mydict['newPassword']
    except:
        return jsonify({"message": "User ID and old password and new password is required."}), 518
    code, msg = auth.change_password(user_id, old_password, new_password)
    return jsonify({"message": msg}), code
    

@bp_auth.route("/logout", methods=["POST"])
def logout():
    try:
        data = request.get_data()
        mydict = json.loads(data)
        user_id = mydict['user_id']
    except:
        return jsonify({"message": "User ID is required."}), 518
    
    if not auth.get_user(user_id):
        return jsonify({"message": "User ID does not exist."}), 401

    token = request.headers.get("token")

    code, msg = auth.logout(user_id, token)
    return jsonify({"message": msg}), code