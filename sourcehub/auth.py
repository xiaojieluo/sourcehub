from hashlib import md5
from functools import wraps
from flask import current_app
from flask_restful import reqparse
from flask_login import LoginManager, login_required
from sourcehub.models import App, User
from sourcehub import error


def authenticate_session(*args, **kw) -> tuple:
    """验证 sessionToken

    Returns:
        tuple: (boolean, str, str)
        第一个参数为 bool 值，标志验证是否成功，成功为 True， 失败为 False
        第二个参数为 str, 当验证成功时返回 None, 验证失败时返回失败信息
    """
    parser = reqparse.RequestParser()
    parser.add_argument('sessionToken', location='headers')
    parser.add_argument('appid', location='headers')
    headers = parser.parse_args()

    sessionToken = headers.get('sessionToken', '')
    user = User.query.filter_by(sessionToken=sessionToken).first()
    if not user:
        return (False, 'sessionToken 无效')

    verify, err_msg = user.verify_sessiontoken(sessionToken)

    current_app.logger.debug(verify)

    if verify:
        return (True, None)
    else:
        return (False, err_msg)


def authenticate_level(*args, **kw):
    """验证 sessionToken 获取用户的权限
    需要数据库字段支持， 0-9 管理员权限
    TODO
    """
    pass


def authenticate_app(*args, **kw) -> tuple:
    """验证 app 权限

    Returns:
        tuple: (boolean, str, str)
        第一个参数为 bool 值，标志验证是否成功，成功为 True， 失败为 False
        第二个参数为 str, 当验证成功时返回 None, 验证失败时返回失败信息
        第三个参数为 str， 表示验证所用的权限， 'normal' 为普通权限， 'master' 为管理员权限
    """
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

    # 获取验证所用权限， normal or master
    method = 'master' if master else 'normal'

    if auth_app:
        key = auth_app.appkey
        if master:
            # 若 master key 存在， 将使用 master key 验证
            key = master
        # 用 key 或 master key 计算 sign
        byte_str = '{}'.format(timestamp + key)
        local_sign = md5(byte_str.encode('utf-8'))
        if sign == local_sign.hexdigest():
            # Sign 验证通过
            return (True, None, method)
    return (False,  'authenticated failed!', method)


def authenticate_masterkey(*args, **kw) -> tuple:
    """验证 app 权限是否是 master key

    Args:
        str ([type]): [description]

    Returns:
        tuple(bool, str): 第一个参数为 bool, 验证成功为 True， 验证失败为False
        第二个参数为 str， 验证成功时为 None, 验证失败时返回失败信息。
    """
    result, err_msg, method = authenticate_app(*args, **kw)
    if result is True and method == 'master':
        current_app.logger.debug("验证成功。")
        return (True, None)
    else:
        return (False, '_authenticate_masterkey: 失败')


def authenticate(*callback, method='and'):
    """验证函数
    Args:
        callback ([type]): [description]
    """
    def auth(func):
        @wraps(func)
        def wrapper(*args, **kw):
            data = {
                'results': list(),
                'err_msg': list(),
            }
            for _func in callback:
                result = _func(*args, **kw)
                try:
                    result, err_msg = _func(*args, **kw)
                except ValueError as e:
                    result, err_msg, _ = _func(*args, **kw)
                data['results'].append(result)
                data['err_msg'].append(err_msg)

            current_app.logger.debug(data)

            if method == 'and':
                if all(data['results']):
                    return func(*args, **kw)
            if method == 'or':
                if any(data['results']):
                    return func(*args, **kw)

            # TODO
            # for err_code in data['err_code']:
            #     return error(err_code)
            return {'err_code': 1, 'err_msg': data['err_msg']}

        return wrapper
    return auth
