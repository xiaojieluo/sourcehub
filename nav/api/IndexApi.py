from flask import Blueprint, current_app
from flask_restful import Resource, Api, reqparse, fields, marshal_with
from .utils import authenticate

app = current_app

index_api = Blueprint('index_api', __name__, url_prefix = '/api')
api = Api(index_api)

# parser = reqparse.RequestParser()
# parser.add_argument('rate', type=int, help="Rate to charge for this resource.")
# args = parser.parse_args()

class APIBase(object):
    def authenticate(self, *args):
        print(args)
        pass


resource_fields = {
    'url': fields.String,
    'index': fields.Url('index_api.token', absolute = True)
}

parser = reqparse.RequestParser()
parser.add_argument('X-Id', location = 'headers', required = True)
parser.add_argument('X-Key', location = 'headers')
parser.add_argument('X-Sign', location = 'headers')

class Token(Resource, APIBase):
    # method_decorators = [authenticate]

    @marshal_with(resource_fields)
    def get(self):
        print(parser.parse_args())
        print(self.authenticate(parser.parse_args()))
        return {'url': 'Fuck', 'token': 'token'}
        # return 'token'

class Index(Resource, APIBase):
    def get(self):
        base_url = 'http://127.0.0.1:5000/api/'
        return {
            'links': '{}links'.format(base_url),
            'users': '{}users'.format(base_url),
            'tags': '{}tags'.format(base_url)
        }

api.add_resource(Token, '/token')
api.add_resource(Index, '/')