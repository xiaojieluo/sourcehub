from flask import Blueprint, current_app, request
from flask_restful import Resource, Api, reqparse
from sourcehub.models import Link
from sourcehub.auth import authenticate
from sourcehub import api_url
import os
import datetime

link_api = Blueprint('link_api', __name__, url_prefix='/api/links')
api = Api(link_api)


class LinkList(Resource):
    decorators = [authenticate]

    def get(self):
        """显示链接列表, 可批量，可加过滤条件

        Returns:
            [type] -- [description]
        """
        # tmps = Link.objects()
        links = [link.to_dict() for link in Link.objects()]
        return {
            'len': len(links),
            'results': links
        }

    def post(self):
        """新建链接

        Returns:
            [type] -- [description]
        """
        args = request.json
        current_app.logger.debug(args)

        try:
            link = Link(**args)
            link.save()

            # 更新 tag 表
            Link.add_tags(link, link.tags)
            # for tag in args['tags']:
            #     Tag.objects(name=tag).update_one(
            #         inc__count=1, push__sites=site.id, upsert=True)

            data = link.to_dict()
            return {
                '_id': data['_id'],
                'created_at': data['created_at'],
            }, 201, {'Location': '{}/links/{}'.format(api_url, data['_id'])}

        except Exception as e:
            current_app.logger.debug(e)
            return {'message': 'error.'}, 400


class Links(Resource):
    method_decorators = {
        'delete': [authenticate, ],
        'get': [authenticate, ]
    }

    def get(self, link_id):
        """获取单条链接详情

        Arguments:
            link_id {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        link = Link.objects(id=link_id).first()
        current_app.logger.debug(link)
        if link:
            return link.to_dict(), 200
        else:
            return {'message': 'link not found!'}, 404

    def delete(self, link_id):
        """按 link_id 删除链接

        Arguments:
            link_id {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        link = Link.objects(id=link_id).first()

        if link:
            link.delete()

        return {'message': 'delete success'}, 200

    def put(self, link_id):
        """更新单条链接

        Arguments:
            link_id {[type]} -- [description]
        """
        link = Link.objects(id=link_id).first()
        if not link:
            return {'message': 'not found this link'}, 404
        try:
            args = request.json
            if 'tags' in args:
                Link.remove_tags(link, link.tags)
                Link.add_tags(link, data['tags'])
            link.update(**args, updated_at=datetime.datetime.now())
            return {'updated_at': link.updated_at.isoformat()}

        except Exception as e:
            current_app.logger.debug(e)
            return {'message': e}, 404


api.add_resource(LinkList, '/')
api.add_resource(Links, '/<link_id>')
