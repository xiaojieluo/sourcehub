from flask import Blueprint
from flask_restful import Resource, Api, reqparse
from nav.models import Link as LinkModel
import os

link_api = Blueprint('link_api', __name__, url_prefix='/api/links')
api = Api(link_api)


class LinkList(Resource):
    def get(self):
        links = LinkModel.objects
        print(links)
        pass

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, help='Bad {error_msg}')
        parser.add_argument('url', type=str, help='cannot blank!')
        parser.add_argument('visit', type=int)
        parser.add_argument('tags', type=str, action='append')

        args = parser.parse_args()
        print(args)


class Links(Resource):
    pass


api.add_resource(LinkList, '/')
api.add_resource(Links, '/<linkid>')
