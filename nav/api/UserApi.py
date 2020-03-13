from nav import app
from flask import Blueprint
from flask_restful import Resource, Api

user_api = Blueprint('user_api', __name__, url_prefix = '/api/users')
api = Api(user_api)

class UserListApi(Resource):
    '''用户列表 api'''
    def get(self):
        return 'users'

class UserApi(Resource):
    '''单个用户 api'''
    def get(self, uid):
        pass

api.add_resource(UserListApi, '')
