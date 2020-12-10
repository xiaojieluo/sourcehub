from flask import Blueprint, current_app, request, jsonify
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from sourcehub.auth import authenticate
from hashlib import md5
from sourcehub.error_code import error_code

app = current_app

index_api = Blueprint('index_api', __name__, url_prefix='/api')
api = Api(index_api)


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
            'resules': results,
        }


api.add_resource(Index, '/')
