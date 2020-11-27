import datetime
from flask import Blueprint, current_app, request, jsonify
from flask_restful import Resource, Api, reqparse
from sourcehub import api_url, db
from sourcehub.auth import authenticate, authenticate_session
from sourcehub.models.site import Site
from sourcehub.models.tag import Tag
import json


site_api = Blueprint('site_api', __name__, url_prefix='/api/sites')
api = Api(site_api)


parser = reqparse.RequestParser()
parser.add_argument('where', type=str, location="args")
parser.add_argument('order', type=str, location="args")

# class Query(object):
#     pass


def explode_order(args):
    order_list = list()
    if args != None:
        order_list = args.split(',')
    return order_list


def explode_where(where_dict):
    """处理url中的 where字段，
    # TODO
    Arguments:
        where_dict {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    res = {}
    if where_dict is None:
        return res
    where = json.loads(where_dict)

    for key, value in where.items():
        # 如果 value 为 dict , 则表示有其他选项参数， 需要进一步处理合并
        if isinstance(value, dict):
            # 处理具体到值的时候
            tmp = ''
            for k, v in value.items():
                # 合并产生新 key 值
                tmp = '{}__{}'.format(key, k.strip('$'))
            res.update({tmp: v})
            current_app.logger.debug(res)
            print(res)
        else:
            res = where
    print(res)
    return res

class APIResource(Resource):
    """继承 Resource , 实现 exclude 和 order 等参数过滤器

    Args:
        Resource ([type]): [description]
    """
    pass

class SiteListApi(Resource):
    method_decorators = {
        'get': [authenticate, ],
    }

    def get(self):
        args = parser.parse_args()
        where = explode_where(args['where'])
        order = explode_order(args['order'])
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

    def post(self):
        """新增站点
        """
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        parser.add_argument('desc')
        parser.add_argument('url', required=True)
        parser.add_argument('tags', action='append')
        # parser.add_argument('author', required=True)
        # parser.add_argument('vote')
        args = parser.parse_args()
        current_app.logger.debug(args)

        tags = args.pop('tags', [])
        site = Site(**args, tags = [])
        db.session.add(site)
        db.session.commit()

        # 更新 tag 表
        current_app.logger.debug("更新 Tags 表")
        for tag in tags:
            t = Tag.query.filter_by(name=tag).first()
            if t is None:
                t = Tag(name = tag, sites = [site.id,])
            else:
                t.sites.append(site.id)
            site.tags.append(t.id)

            db.session.add(t)
            db.session.add(site)
        db.session.commit()

        return {
            "status": "Success."
        }

        try:
            site = Site(**args)
            site.save()

            # 更新 tag 表
            for tag in args['tags']:
                Tag.objects(name=tag).update_one(
                    inc__count=1, push__sites=site.id, upsert=True)

            data = site.to_dict()
            return {
                '_id': data['_id'],
                'created_at': data['created_at'],
            }, 201, {'Location': '{}/sites/{}'.format(api_url, data['_id'])}

        except Exception as e:
            current_app.logger.debug(e)
            return {'message': 'error.'}, 400


class SiteApi(Resource):
    method_decorators = {
        'delete': [authenticate, ]
    }

    def get(self, site_id):
        site = Site.objects(id=site_id).first()

        if site:
            data = site.to_dict()
            author = User.objects(id=data['author']).first()
            if author:
                data['author'] = {'_id': str(
                    author.id), 'name': author.username}
            return data, 200

    def delete(self, site_id):
        """删除 site

        Arguments:
            site_id {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        site = Site.objects(id=site_id).first()

        if site:
            # 删除 tag 表的记录
            for tag in site.tags:
                Tag.objects(name=tag).update_one(
                    dec__count=1, pull__sites=site.id, upsert=True)
            site.delete()

        return {'message': 'success'}, 200

    def put(self, site_id):
        """更新 site

        Arguments:
            site_id {[type]} -- [description]
        """
        site = Site.objects(id=site_id).first()

        if not site:
            return {'message': 'not found site'}, 404

        try:
            data = request.json
            # 更新 tags 表
            # 因为这里是覆盖更新，所以需要删除之前 tags 的所有关联数据，再重新写入新的 tags 数据
            if 'tags' in data:
                Tag.remove_tags(site, site.tags)
                Tag.add_tags(site, data['tags'])

            site.update(**data, updated_at=datetime.datetime.now())
            return {'updated_at': site.updated_at.isoformat()}

        except Exception as e:
            current_app.logger.debug(e)
            return {'message': e}, 404


api.add_resource(SiteListApi, '/')
api.add_resource(SiteApi, '/<site_id>')
