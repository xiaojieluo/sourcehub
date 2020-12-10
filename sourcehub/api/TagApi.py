import datetime
from flask import Blueprint, current_app, request
from flask_restful import Resource, Api, reqparse
from sourcehub import api_url, error
from sourcehub.database import db
from sourcehub.auth import authenticate, authenticate_session, authenticate_app, authenticate_masterkey
from sourcehub.models import Tag, Site, Link

tag_api = Blueprint('tag_api', __name__)
api = Api(tag_api)


class TagListApi(Resource):
    method_decorators = [authenticate(authenticate_app), ]

    def get(self):
        tags = [tag.to_dict() for tag in Tag.query.filter_by().all()]

        return {
            'len': len(tags),
            'results': tags
        }


class TagApi(Resource):
    method_decorators = [authenticate(authenticate_app)]

    def get(self, tag_id):
        """获取标签信息

        Arguments:
            tag_id {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        try:
            tag_id = int(tag_id)
        except ValueError as e:
            return error(101)

        tag = Tag.query.filter_by(id=tag_id).first()
        if tag:
            return tag.to_dict(), 200
        else:
            return {'message': "Not found"}, 404

    @authenticate(authenticate_masterkey)
    def delete(self, tag_id):
        try:
            tag_id = int(tag_id)
        except ValueError as e:
            return error(104)

        tag = Tag.query.filter_by(id=tag_id).first()

        # 删除 sites 表关联数据
        sites = Site.query.filter(Site.id.in_(tag.sites)).all()
        for site in sites:
            site.tags.remove(tag.id)

        # 删除 links 表关联数据
        links = Link.query.filter(Link.id.in_(tag.links)).all()
        for link in links:
            link.tags.remove(tag.id)

        # 删除 tag 表记录
        db.session.delete(tag)

        # 向数据库提交更改
        db.session.commit()

        return {
            'message': 'success'
        }

    @authenticate(authenticate_masterkey)
    def put(self, tag_id):
        """更新标签信息

        Arguments:
            tag_id {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        try:
            tag_id = int(tag_id)
        except ValueError as e:
            return error(104)

        tag_query = Tag.query.filter_by(id=tag_id)
        if tag_query.first() is None:
            return error(101)

        body = request.json or {}
        try:
            tag_query.update(body)
            db.session.commit()
            return {'updated_at': datetime.datetime.now().isoformat()}
        except Exception as e:
            return {'msg': e.message}


api.add_resource(TagListApi, '/')
api.add_resource(TagApi, '/<tag_id>')
