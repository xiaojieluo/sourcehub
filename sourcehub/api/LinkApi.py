from flask import Blueprint, current_app, request
from flask_restful import Resource, Api, reqparse
from sourcehub import db
from sourcehub.models import Link, User, Tag
from sourcehub.auth import authenticate, authenticate_app, authenticate_masterkey, authenticate_session
from sourcehub import api_url, error
import os
import datetime

link_api = Blueprint('link_api', __name__)
api = Api(link_api)


class LinkList(Resource):
    method_decorators = [authenticate(authenticate_app)]

    def get(self):
        """显示链接列表, 可批量，可加过滤条件

        Returns:
            [type] -- [description]
        """
        links = [link.to_dict() for link in Link.query.all()]
        return {
            'len': len(links),
            'results': links
        }

    @authenticate(authenticate_session)
    def post(self):
        """新建链接

        Returns:
            [type] -- [description]
        """
        parser = reqparse.RequestParser()
        parser.add_argument('sessionToken', location='headers')
        headers = parser.parse_args()

        data = request.json
        current_app.logger.debug(data)

        tags = data.pop('tags', [])
        sessionToken = headers.pop('sessionToken', '')

        user = User.query.filter_by(sessionToken=sessionToken).first()
        data['author_id'] = user.id
        try:
            link = Link(**data)
            db.session.add(link)
            db.session.commit()
        except TypeError as e:
            return {'err_msg': e.args}

        # 将用户新建的 site id 写入 user.sites
        if link.id not in user.links:
            user.sites.append(link.id)
            db.session.commit()

        for tag in tags:
            t = Tag.query.filter_by(name=tag).first()
            if t is None:
                t = Tag(name=tag, links=[link.id, ])
            else:
                t.links.append(link.id)

            db.session.add(t)
            db.session.commit()

            link.tags.append(t.id)
            db.session.commit()

        return {
            'id': link.id,
            'created_at': link.to_dict().get('created_at'),
        }, 201, {'Location': f'{api_url}/links/{link.id}'}


class Links(Resource):
    method_decorators = [authenticate(authenticate_app), ]

    def get(self, link_id):
        """获取单条链接详情

        Arguments:
            link_id {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        try:
            link_id = int(link_id)
        except ValueError as e:
            return error(104)

        link = Link.query.filter_by(id=link_id).first()
        current_app.logger.debug(link)
        if link:
            return link.to_dict(), 200
        else:
            return error(101)
            return {'message': 'link not found!'}, 404

    @authenticate(authenticate_session, authenticate_masterkey, method='or')
    def delete(self, link_id):
        """删除链接
        只允许创建者和 master_key 有权限操作

        Arguments:
            link_id {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        try:
            link_id = int(link_id)
        except ValueError as e:
            return error(104)

        link = Link.query.filter_by(id=link_id).first()
        if not link:
            return error(101)

        tags = Tag.query.filter(Tag.id.in_(link.tags)).all()
        for tag in tags:
            try:
                tag.links.remove(link.id)
            except ValueError as e:
                current_app.logger.debug(
                    f"Tag id:{tag} not in tag.sites: {tag.links}")

        # 从 user.sites 字段中删除关联数据
        user = User.query.filter_by(id=link.author_id).first()
        if user:
            user.sites.remove(link.id)

        db.session.delete(link)
        db.session.commit()

        return {'message': 'success'}, 200

    @authenticate(authenticate_session, authenticate_masterkey, method='or')
    def put(self, link_id):
        """更新单条链接
        只允许创建者和持有 master_key 密钥的有权限更新

        Arguments:
            link_id {[type]} -- [description]
        """
        try:
            link_id = int(link_id)
        except ValueError as e:
            return error(104)

        data = request.json
        if data is None or not isinstance(data, dict):
            current_app.logger.warning("更新用户 body 为空")
            data = dict()

        link = Link.query.filter_by(id=link_id).first()
        if not link:
            return error(101)

        if 'tags' in data.keys():
            # 遍历查询 site 关联的 tag 表， 从 tag 表中删除关联的数据
            tags = Tag.query.filter(Tag.id.in_(link.tags)).all()
            for tag in tags:
                if link.id in tag.links:
                    tag.links.remove(link.id)
            db.session.commit()
            # 遍历用户传入的 tags 字段，写入 tag 表，并关联 site 数据
            tag_list_ids = list()
            # tags_str = data.pop('tags')
            for tag in data.pop('tags', []):
                t = Tag.query.filter_by(name=tag).first()
                if t is None:
                    t = Tag(name=tag, links=[link.id, ])
                if link.id not in t.links:
                    t.sites.append(link.id)
                db.session.add(t)
                db.session.commit()
                tag_list_ids.append(t.id)
            link.tags = tag_list_ids

        try:
            link.updated_at = datetime.datetime.now()
            Link.query.filter_by(id=link.id).update(data)
            db.session.commit()
            return {
                'updated_at': str(link.updated_at),
            }
        except Exception as e:
            print(e)
            return error(-1)


api.add_resource(LinkList, '/')
api.add_resource(Links, '/<link_id>')
