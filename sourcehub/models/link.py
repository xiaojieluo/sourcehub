import datetime
from sourcehub import db
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import class_mapper
from sourcehub.database import MutableList, ModelMixin


class Link(ModelMixin, db.Model):
    __tablename__ = 'links'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    # 网站简介
    desc = db.Column(db.String(255))
    url = db.Column(db.String(255))
    # Tag 数组， 一维数组
    tags = db.Column(
        MutableList.as_mutable(postgresql.ARRAY(db.Integer, dimensions=1)),
        server_default='{}',
        default=list(),
    )
    # 网站首页图片
    pic = db.Column(db.String(255))
    # image = StringField(default='')
    vote = db.Column(db.Integer, default=0)
    star = db.Column(db.Integer, default = 0)
    # Slug , URL 缩写， 如果不存在的话就使用 _id 来当作 URL, 建议设置，有利于 SEO, 唯一不重复的字符串
    slug = db.Column(db.String(255), default=None)
    # 收藏者
    followers = db.Column(
        MutableList.as_mutable(postgresql.ARRAY(db.Integer, dimensions=1)),
        server_default='{}',
        default=list(),
    )
    # 提交者id
    author_id = db.Column(db.Integer)
    created_at = db.Column(db.TIMESTAMP, default = datetime.datetime.now())
    updated_at = db.Column(db.TIMESTAMP, default = datetime.datetime.now())