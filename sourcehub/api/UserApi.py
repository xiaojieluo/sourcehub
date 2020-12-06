import datetime
from flask import Blueprint, current_app, request
from flask_restful import abort, Api, reqparse, Resource
from sourcehub import api_url, db, error
from sourcehub.auth import authenticate, authenticate_key, authenticate_masterkey, authenticate_session
from sourcehub.models import User


user_api = Blueprint('user_api', __name__)
api = Api(user_api)


class UserListApi(Resource):
    '''用户列表 api'''
    method_decorators = {
        'get': [authenticate(authenticate_key)]
    }

    def get(self):
        """显示 用户列表
        GET /users/

        Returns:
            [list] -- [description]
        """
        users = [user.to_dict() for user in User.query.all()]
        current_app.logger.debug(users)
        return {
            'err_code': 0,
            'len': len(users),
            'results': users
        }

    def post(self):
        """注册用户
        POST /users/

        Returns:
            [dict] -- [description]
        """
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, help='Bad {error_msg}')
        parser.add_argument('password', type=str, help='cannot blank!')
        parser.add_argument('phone', type=str, help='input phone number')
        parser.add_argument('email', type=str)
        args = parser.parse_args()

        if User.query.filter_by(username=args['username']).first() is not None:
            # 用户名已经存在
            msg = '用户名已经存在'
            current_app.logger.debug("用户名已存在")
            return msg

        try:
            user = User(username=args['username'],
                        phone=args['phone'], email=args['email'])
            user.hash_password(args['password'])
            user.generate_sessiontoken()
            db.session.add(user)
            db.session.commit()
            return {
                'err_code': 0,
                'data': {
                    'sessionToken': user.sessionToken,
                    'created_at': str(user.created_at),
                    '_id': user.id
                }
            }, 201, {'Location': '{}/users/{}'.format(api_url, user.id)}
        except Exception as e:
            print(type(e))
            print(current_app.config['SECRET_KEY'])
            current_app.logger.debug("注册用户失败：{}".format(e))
            result = {
                'message': e.__str__(),
                'code': '1001'
            }
            return result


class UserApi(Resource):
    '''单个用户 api'''

    method_decorators = {
        'delete': [authenticate(authenticate_key)]
    }

    def get(self, user_id):
        """获取用户信息

        Arguments:
            user_id {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        user = User.query.filter_by(id=user_id).first()
        result = {}
        if user:
            result = user.to_dict()
            return result, 200
        else:
            return {'message': 'get error.'}, 404

    @authenticate(authenticate_session, authenticate_masterkey, method='or')
    def put(self, user_id):
        """更新指定用户信息

        Arguments:
            user_id {[type]} -- [description]
        """
        data = request.json
        if request.json is None or isinstance(request.json, dict):
            current_app.logger.warning("更新用户 body 为空")
            data = dict()

        data['updated_at'] = datetime.datetime.now()
        try:
            # 更新用户字段
            user = User.query.filter_by(id=user_id).update(data)
            db.session.commit()
            return {'updated_at': str(data['updated_at'])}
        except Exception as e:
            current_app.logger.debug(e)
            return {'err_code': 1, 'err_msg': f'更新用户信息失败： {e}'}

    @authenticate(authenticate_session, authenticate_masterkey, method='or')
    def delete(self, user_id):
        """
        使用有效的 sessionToken 或者 masterkey 都可以删除用户

        无论是否找到指定用户，都会返回 删除成功信息。
        Arguments:
            user_id {[type]} -- [description]
        """
        User.query.filter_by(id=user_id).update({"activity": 0})
        db.session.commit()

        return {'message': 'success'}, 200


class UserLoginApi(Resource):
    """用户登录

    Arguments:
        Resource {[type]} -- [description]
    """
    method_decorators = {
        'get': [authenticate(authenticate_key)]
    }

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, help='username')
        parser.add_argument('email', type=str, help='email')
        parser.add_argument('password', type=str)
        args = parser.parse_args()

        user = User.query.filter_by(username=args['username']).first()
        if not user:
            user = User.query.filter_by(email=args['email']).first()

        if not user:
            return {'message': '用户不存在', 'err_code': 404}, 404

        if user.activity != 1:
            return {
                'message': '用户已注销，无法登陆',
                'err_code': 401
            }, 404

        if user.verify_password(args['password']):
            user.last_login = datetime.datetime.now()
            user.generate_sessiontoken(3600)
            return user.to_dict(), 200
        else:
            return {
                'message': 'colud not find user',
                'err_code': 404
            }, 404


class RefreshSessionToken(Resource):
    """重置用户的 sessionToken
    调用这个 API 要求传入登陆时返回的 sessionToken 作为认证，或者使用 MAster Key

    Arguments:
        Resource {[type]} -- [description]
    """

    @authenticate(authenticate_session, authenticate_masterkey, method='or')
    def put(self, user_id):
        """重置用户的 sessionToken
            调用这个 API 要求传入登陆时返回的 sessionToken 作为认证，或者使用 Master Key

        Args:
            user_id (int): [description]

        Returns:
            [type]: [description]
        """
        parser = reqparse.RequestParser()
        parser.add_argument('expire_in', type=int)
        args = parser.parse_args()
        print(args)
        user = User.query.filter_by(id=user_id).first()

        if user:
            user.generate_sessiontoken()
        data = user.to_dict()

        return data, 200


class UserMeApi(Resource):
    """GET /users/me
    通过 sessionToken 获取用户信息

    Args:
        Resource ([type]): [description]

    Returns:
        [type]: [description]
    """
    @authenticate(authenticate_key, authenticate_session, method='and')
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('sessionToken', location='headers', type=str)
        headers = parser.parse_args()

        sessionToken = headers['sessionToken']
        current_app.logger.debug(sessionToken)

        user = User.query.filter_by(sessionToken=sessionToken).first()
        if user:
            return user.to_dict(), 200
        else:
            return {
                'err_code': 1,
                'err_msg': '未找到用户。'
            }


api.add_resource(UserListApi, '/')
api.add_resource(UserMeApi, '/me')
api.add_resource(UserApi, '/<user_id>')
api.add_resource(UserLoginApi, '/login')
api.add_resource(RefreshSessionToken, '/<user_id>/refreshSessionToken')
