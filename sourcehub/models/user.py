from sourcehub import db
from datetime import datetime
import uuid
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from sqlalchemy.orm import class_mapper


class User(db.Model):
    """用户表

    Args:
        db ([type]): [description]
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    # 登录凭证
    sessionToken = db.Column(db.String(255))
    # 标星的链接
    # star = ListField(ReferenceField('Link'))
    created_at = db.Column(db.TIMESTAMP, default=datetime.now())
    updated_at = db.Column(db.TIMESTAMP, default=datetime.now())
    # 最后登录时间
    last_login = db.Column(db.TIMESTAMP, default=datetime.now())
    # 帐号活跃值，当用户注销账号时，将值设置为0，即冻结状态
    activity = db.Column(db.Integer, default=1)

    def to_dict(self, found=None):
        """将查询返回的字段转换成 dict 格式
        copyright [stackoverflow](https://stackoverflow.com/questions/23554119/convert-sqlalchemy-orm-result-to-dict)

        Args:
            self (object): [description]
            found ([type], optional): [description]. Defaults to None.

        Returns:
            [type]: [description]
        """
        if found is None:
            found = set()
        mapper = class_mapper(self.__class__)
        columns = [column.key for column in mapper.columns]
        get_key_value = lambda c: (c, getattr(self, c).isoformat()) if isinstance(getattr(self, c), datetime) else (c, getattr(self, c))
        out = dict(map(get_key_value, columns))
        for name, relation in mapper.relationships.items():
            if relation not in found:
                found.add(relation)
                related_obj = getattr(self, name)
                if related_obj is not None:
                    if relation.uselist:
                        out[name] = [self.to_dict(child, found) for child in related_obj]
                    else:
                        out[name] = self.to_dict(related_obj, found)

        out.pop('password_hash')
        return out

    def generate_sessiontoken(self, expiration_time=604800):
        """生成 User 的 sessionToken

        Args:
            expiration_time (int): sessionToken的过期时间，单位为秒，默认是 604800，即7天.
                如果值为None,则 sessionToken 无过期限制
        """
        secret_key = current_app.config['SECRET_KEY']
        print(secret_key)
        current_app.logger.debug(f"secret_key = {secret_key}")

        if expiration_time is None:
            expiration_time = 315569260
        s = Serializer(secret_key, expiration_time)

        self.sessionToken = s.dumps(self.id).decode('utf-8')

    def verify_sessiontoken(self, token) -> tuple:
        """验证 sessionToken
            校验 sessionToken 分两步
            1. 先校验从 api 中传入的 token 与数据库中存储的 sessionToken 是否相等
            2. 校验 sessionToken 的数据有效性和时间有效性
            这两步顺序执行

        Returns:
            tuple: 验证成功返回 (True, None)， 失败返回 (False, 失败信息)
        """
        result = (False, None)
        if token != self.sessionToken:
            return result

        secret_key = current_app.config['SECRET_KEY']
        current_app.logger.debug(f"secret_key is {secret_key}")
        s = Serializer(secret_key)
        try:
            data = s.loads(token.encode('utf-8'))
            if data == self.id:
                result = (True, None)
        except Exception as e:
            current_app.logger.debug(e)
            result = (False, e)

        return result

    def hash_password(self, password):
        """hash 密码加密

        Args:
            password (str): 未加密的密码
        """
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password) -> bool:
        """hash 密码验证

        Args:
            password (str): 用户传入的未加密的密码

        Returns:
            bool: 验证成功返回 True, 失败返回False
        """
        return pwd_context.verify(password, self.password_hash)
