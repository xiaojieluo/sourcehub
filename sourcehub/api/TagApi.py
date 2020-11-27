import datetime
from flask import Blueprint, current_app, request
from flask_restful import Resource, Api, reqparse
from sourcehub import api_url
from sourcehub.auth import authenticate, authenticate_session
from sourcehub.models import Tag

tag_api = Blueprint('tag_api', __name__, url_prefix='/api/tags')
api = Api(tag_api)


class TagListApi(Resource):
    method_decorators = {
        'get': [authenticate, ]
    }

    def get(self):
        tags = [tag.to_dict() for tag in Tag.objects()]

        return {
            'len': len(tags),
            'results': tags
        }


class TagApi(Resource):

    decorators = [authenticate,]

    def get(self, tag_id):
        """获取标签信息

        Arguments:
            tag_id {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        tag = Tag.objects(id=tag_id).first()
        if tag:
            return tag.to_dict()
        else:
            return {'message': "Not found"}, 404

    def put(self, tag_id):
        """更新标签信息

        Arguments:
            tag_id {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        tag = Tag.objects(id=tag_id).first()
        if tag:
            body = request.json or {}

            print(body)

            tag.update(**body)
            return {'updated_at': datetime.datetime.now().isoformat()}
        else:
            return {'error': 'not found.'}, 404


api.add_resource(TagListApi, '/')
api.add_resource(TagApi, '/<tag_id>')
