import datetime
from flask import Blueprint, current_app, request
from flask_restful import Resource, Api, reqparse
from sourcehub import api_url
from sourcehub.auth import authenticate, authenticate_session
from sourcehub.models import User


user_api = Blueprint('user_api', __name__, url_prefix='/api/users')
api = Api(user_api)


class UserListApi(Resource):
    '''用户列表 api'''
    method_decorators = {
        'get': [authenticate]
    }

    def get(self):
        """显示 用户列表
        GET /users/

        Returns:
            [list] -- [description]
        """
        # 过滤 password 不显示
        tmp = User.objects()
        users = [user.to_dict() for user in tmp]
        print(users)
        return users
        return {
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

        try:
            user = User(**args)
            user.save()
            user.generateSessionToken()

            data = user.to_dict()
            result = {
                'sessionToken': data['sessionToken'],
                'created_at': data['created_at'],
                '_id': data['_id'],
            }
            return result, 201, {'Location': '{}/users/{}'.format(api_url, data['_id'])}
        except Exception as e:
            current_app.logger.debug("注册用户失败：{}".format(e))
            result = {
                'message': e.__str__(),
                'code': '1001'
            }
            return result


class UserApi(Resource):
    '''单个用户 api'''

    method_decorators = {
        'delete': [authenticate]
    }

    def get(self, user_id):
        """获取用户信息

        Arguments:
            user_id {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        user = User.objects(id=user_id).first()
        result = {}
        if user:
            result = user.to_dict()
            return result, 200
        else:
            return {'message': 'get error.'}, 404

    @authenticate_session
    def put(self, user_id):
        """更新指定用户信息

        Arguments:
            user_id {[type]} -- [description]
        """
        user = User.objects(id=user_id).first()
        if user:
            update_data = request.json
            try:
                # 更新用户字段
                user.update(**update_data, updated_at=datetime.datetime.now())
                return {'updated_at': user.updated_at.isoformat()}
            except Exception as e:
                current_app.logger.debug(e)

    @authenticate_session
    def delete(self, user_id):
        """
        TODO
        删除用户需要 X-SH-Session 验证, 或者用 Master key 强制删除

        无论是否找到指定用户，都会返回 删除成功信息。
        Arguments:
            user_id {[type]} -- [description]
        """
        user = User.objects(id=user_id).first()
        if user:
            user.delete()

        return {'message': 'success'}, 200


class UserLoginApi(Resource):
    """用户登录

    Arguments:
        Resource {[type]} -- [description]
    """
    method_decorators = {
        'get': [authenticate]
    }

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, help='username')
        parser.add_argument('email', type=str, help='email')
        parser.add_argument('password', type=str)
        args = parser.parse_args()

        user = User.objects(username=args['username']).first()
        if not user:
            user = User.ojects(email=args['email']).first()

        if user and user.password == args['password']:
            # 更新登录时间
            user.last_login = datetime.datetime.now()
            user.save()
            result = user.to_dict()
            return result, 200
        else:
            return {'message': 'could not find user.'}, 404


class RefreshSessionToken(Resource):
    """重置用户的 sessionToken
    需要用户原来的 sessionToken 来验证
    Arguments:
        Resource {[type]} -- [description]
    """

    @authenticate_session
    def put(self, user_id):
        user = User.objects(id=user_id).first()

        if user:
            user.generateSessionToken()

        data = user.to_dict()

        return data, 200


api.add_resource(UserListApi, '/')
api.add_resource(UserApi, '/<user_id>')
api.add_resource(UserLoginApi, '/login')
api.add_resource(RefreshSessionToken, '/<user_id>/refreshSessionToken')
