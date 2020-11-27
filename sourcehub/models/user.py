from sourcehub import db
import datetime
import uuid


class User(db.Model):
    """用户表

    Args:
        db ([type]): [description]
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    # 登录凭证
    sessionToken = db.Column(db.String(255))
    # 标星的链接
    # star = ListField(ReferenceField('Link'))
    created_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now())
    updated_at = db.Column(db.TIMESTAMP, default=datetime.datetime.now())
    # 最后登录时间
    last_login = db.Column(db.TIMESTAMP, default=datetime.datetime.now())
