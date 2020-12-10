from flask import Flask, jsonify, current_app
from flask_login import LoginManager, login_required
from flask_cors import *
from sourcehub import routes
from flask_sqlalchemy import SQLAlchemy
from sourcehub.define import errors
from functools import wraps
import time
from sourcehub.database import db


api_url = 'http://localhost:5000'


def error(err_code: int, status_code: int = 0, headers: dict = None) -> dict:
    """根据错误码返回错误信息

    Args:
        err_code (int): [description]

    Returns:
        dict: [description]
    """
    err_msg = errors.get(err_code, 'Unknow error.')
    if not isinstance(status_code, int):
        status_code = 200

    if not isinstance(headers, dict):
        headers = dict()

    return {
        'err_code': err_code,
        'err_msg': err_msg
    }, status_code, headers


def make_app():
    app = Flask(__name__)
    app.port = 5000
    app.secret_key = 'Security!'
    app.config['BUNDLE_ERRORS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://sourcehub:sourcehub@localhost/sourcehub'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SQLALCHEMY_ECHO"] = True

    CORS(app)

    db.init_app(app)
    routes.init_app(app)

    return app
