from flask import Blueprint, current_app, request
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from .utils import authenticate
from functools import wraps
from sourcehub.auth import authenticate
# from sourcehub.models import Auth
from hashlib import md5
from sourcehub.error_code import error_code

app = current_app

index_api = Blueprint('index_api', __name__, url_prefix='/api')
api = Api(index_api)


resource_fields = {
    'url': fields.String,
    'index': fields.Url('index_api.token', absolute=True)
}


class Token(Resource):

    method_decorators = {
        'get': [authenticate]
    }

    @marshal_with(resource_fields)
    def get(self):
        return {'url': 'Fuck', 'token': 'token'}


class Index(Resource):

    def get(self):
        """ GET /api/

        Returns:
            [type]: [description]
        """
        app.logger.debug(request.headers)

        base_url = 'http://127.0.0.1:5000/api'
        results = {
            'links': '{}/links'.format(base_url),
            'users': '{}/users'.format(base_url),
            'tags': '{}/tags'.format(base_url)
        }
        return {
            'error_code': error_code(0),
            'resules':results,
            }


api.add_resource(Token, '/token')
api.add_resource(Index, '/')
