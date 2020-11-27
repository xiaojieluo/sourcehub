from flask_login import LoginManager, login_required
from flask_restful import reqparse
from flask import current_app
from functools import wraps
from hashlib import md5
from sourcehub.models import App
from sourcehub.models import User


def authenticate(func, auth_session=False):
    """验证 app 的 api 请求权限

    Arguments:
        func {[type]} -- [description]

    Raises:
        Exception: [description]

    Returns:
        [type] -- [description]
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        parser = reqparse.RequestParser()
        parser.add_argument('appid', location='headers', required=True)
        parser.add_argument('appkey', location='headers')
        parser.add_argument('appsign', location='headers')
        headers = parser.parse_args()
        current_app.logger.debug(headers)

        appsign = headers['appsign'] or ','
        appsign += ','
        sign, timestamp, master = appsign.split(',')[0:3]
        current_app.logger.debug(appsign)

        if not master:
            master = None

        appid = headers['appid']
        auth_app = App.query.filter_by(appid=appid).first()

        if auth_app:
            key = auth_app.appkey
            if master:
                # 若 master key 存在， 将使用 master key 验证
                key = master
            # 用 key 或 master key 计算 sign
            byte_str = '{}'.format(key + timestamp)
            local_sign = md5(byte_str.encode('utf-8'))
            if sign == local_sign.hexdigest():
                # Sign 验证通过
                return func(*args, **kwargs)
        return {'message': 'authenticated failed!'}
    return wrapper


def authenticate_session(func):
    """验证 sessionToken

    TODO
    这个验证必须要 user_id ,可能后期会改进
    Arguments:
        func {[type]} -- [description]
    """
    @wraps(func)
    def wrapper(*args, **kw):
        if 'user_id' not in kw:
            raise Exception('authenticated sessionToken failed.')

        parser = reqparse.RequestParser()
        parser.add_argument('appsession', location='headers')
        parser.add_argument('appid', location='headers')
        headers = parser.parse_args()

        sessionToken = headers.get('appsession', '')
        # user = User.objects(sessionToken=sessionToken).first()
        user = User.query.filter_by(sessionToken=sessionToken).first()

        if user and str(user.id) == kw['user_id']:
            return func(*args, **kw)
        else:
            return {
                'message': 'authenticated sessionToken failed.',
                'code': 2002
            }
    return wrapper


def init_app(login_manager, app):
    # login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login.html'
    login_manager.login_message = 'Unauthorized User'
    login_manager.login_message_category = "info"


def export_sign(data: str) -> str:
    """解析 X-SH-Sign
    """
    print(data)
    data += ','
    sign, timestamp, master = data.split(',')[0:3]

    if not master:
        master = None

    return sign, timestamp, master


def auth_sign(sign, timestamp, master):
    """验证 X-SH-Sign

    Arguments:
        sign {[type]} -- [description]
        timestamp {[type]} -- [description]
        master {[type]} -- [description]
    """
    pass
