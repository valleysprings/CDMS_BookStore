#!/usr/bin/env python3
import os
import logging
from flask import Flask
from flask import request
from be.view import (auth, buyer, seller)
from be.service.db_init import init_app


def create_app(test_config=None):
    # create and configure the app

    app = Flask(__name__, instance_relative_config=True)

    # 关闭服务器
    @app.route('/shutdown', methods=['GET'])
    def shudown():
        func = request.environ.get("werkzeug.server.shutdown")
        if func is None:
            raise RuntimeError("Not running with the Werkzeug Server")
        func()
        return 'Server shutting down...'
    
    init_app(app)

    # blueprint    
    app.register_blueprint(auth.bp_auth)
    app.register_blueprint(buyer.bp_buyer)
    app.register_blueprint(seller.bp_seller)

    return app

if __name__ == 'be':
    app = create_app()