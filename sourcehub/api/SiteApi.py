import json
import datetime
from flask import Blueprint, current_app, request, jsonify
from flask_restful import Resource, Api, reqparse
from sourcehub import api_url, db
from sourcehub.auth import authenticate, authenticate_session, authenticate_app, authenticate_masterkey
from sourcehub.models import Site, Tag, User
from sourcehub import error


site_api = Blueprint('site_api', __name__)
api = Api(site_api)


class SiteListApi(Resource):
    method_decorators = authenticate(authenticate_app)

    def get(self):
        """获取site列表

        Returns:
            [type] -- [description]
        """

        sites = [site.to_dict() for site in Site.query.all()]
        current_app.logger.debug(sites)

        return {
            'len': len(sites),
            'results': sites
        }

    @authenticate(authenticate_session)
    def post(self):
        """新增站点
        """
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        parser.add_argument('desc')
        parser.add_argument('url', required=True)
        parser.add_argument('tags', action='append')
        parser.add_argument('sessionToken', location='headers')
        args = parser.parse_args()
        current_app.logger.debug(args)

        tags = args.pop('tags', [])
        sessionToken = args.pop('sessionToken', '')

        user = User.query.filter_by(sessionToken=sessionToken).first()
        data = args
        data['author_id'] = user.id
        site = Site(**args)
        db.session.add(site)
        db.session.commit()

        # 将用户新建的 site id 写入 user.sites
        if site.id not in user.sites:
            user.sites.append(site.id)
            db.session.commit()

        for tag in tags:
            t = Tag.query.filter_by(name=tag).first()
            if t is None:
                t = Tag(name=tag, sites=[site.id, ])
            else:
                t.sites.append(site.id)

            db.session.add(t)
            db.session.commit()

            site.tags.append(t.id)
            db.session.commit()

        return {
            'id': site.id,
            'created_at': site.to_dict().get('created_at'),
        }, 201, {'Location': f'{api_url}/sites/{site.id}'}


class SiteApi(Resource):
    method_decorators = authenticate(authenticate_app)

    def get(self, site_id):
        try:
            site_id = int(site_id)
        except ValueError as e:
            return error(104)

        site = Site.query.filter_by(id=site_id).first()
        if site:
            data = site.to_dict()
            return data, 200
        else:
            return error(101)

    def delete(self, site_id: int):
        """删除 site
        删除 tag.sites 关联的数据
        删除 user.sites 关联的字段

        Arguments:
            site_id {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        try:
            site_id = int(site_id)
        except ValueError as e:
            return error(104)

        site = Site.query.filter_by(id=site_id).first()
        if not site:
            return error(101)

        tags = Tag.query.filter(Tag.id.in_(site.tags)).all()
        for tag in tags:
            try:
                tag.sites.remove(site.id)
            except ValueError as e:
                current_app.logger.debug(
                    f"Tag id:{tag} not in tag.sites: {tag.sites}")

        # 从 user.sites 字段中删除关联数据
        user = User.query.filter_by(id=site.author_id).first()
        if user:
            user.sites.remove(site.id)

        db.session.delete(site)
        db.session.commit()

        return {'message': 'success'}, 200

    def put(self, site_id: int):
        """更新 site,
        注意： 这个方法为覆盖更新， 只更新传入的字段，其余不变

        Arguments:
            site_id {[type]} -- [description]
        """
        data = request.json
        if data is None or not isinstance(data, dict):
            current_app.logger.warning("更新用户 body 为空")
            data = dict()

        site = Site.query.filter_by(id=site_id).first()
        if not site:
            return error(101)

        # 遍历查询 site 关联的 tag 表， 从 tag 表中删除关联的数据
        tags = Tag.query.filter(Tag.id.in_(site.tags)).all()
        for tag in tags:
            if site.id in tag.sites:
                tag.sites.remove(site.id)
        db.session.commit()

        # 遍历用户传入的 tags 字段，写入 tag 表，并关联 site 数据
        tag_list_ids = list()
        # tags_str = data.pop('tags')
        for tag in data.pop('tags', []):
            t = Tag.query.filter_by(name=tag).first()
            if t is None:
                t = Tag(name=tag, sites=[site.id, ])
            if site.id not in t.sites:
                t.sites.append(site.id)
            db.session.add(t)
            db.session.commit()
            tag_list_ids.append(t.id)

        try:
            site.tags = tag_list_ids
            site.updated_at = datetime.datetime.now()
            Site.query.filter_by(id=site.id).update(data)
            db.session.commit()
            return {
                'updated_at': str(site.updated_at),
            }
        except Exception as e:
            print(e)
            return error(-1)


api.add_resource(SiteListApi, '/')
api.add_resource(SiteApi, '/<site_id>')
