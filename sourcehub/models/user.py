from mongoengine import Document, StringField, DateTimeField, ListField, ReferenceField
import datetime
from sourcehub import login_manager
from flask import current_app
from flask_login import login_user, UserMixin

class User(Document, UserMixin):
    username = StringField(required = True, unique = True)
    email = StringField(required = True)
    password = StringField(required = True)
    # 标星的链接
    star = ListField(ReferenceField('Link'))
    created_at = DateTimeField(default = datetime.datetime.now())
    updated_at = DateTimeField(default = datetime.datetime.now())

    @classmethod
    def register(cls, data):
        '''
        Args:
            data: 脏数据， 需清洗
        '''
        fields = [k for k in cls._fields.keys() if k != 'id']
        user_info = {k: v for k, v in data.items() if k in fields}

        try:
            user = cls(**user_info)
            user.save()
            return user
        except Exception as e:
            current_app.logger.debug(e)
            return None

    @classmethod
    def login(cls, data, **kw):
        '''
        Args:
            data: 用户信息， 包含必须数据
            user: 传入 user 对象， 省略查询， 直接登陆
        '''
        fields = [k for k in cls._fields.keys() if k != 'id']
        user_info = {k: v for k, v in data.items() if k in fields}

        user = cls.objects(**user_info).first()
        if user is None:
            app.logger.info("找不到用户:{}".format(data))
            return False

        try:
            login_user(user, **kw)
            return user
        except Exception as e:
            app.logger.debug("登陆失败：{}".format(e))

    def is_active(self):
        return True

    def do_star(self, link):
        '''执行 star 操作
        Args:
            link: Model object.
        '''
        try:
            self.update(add_to_set__star = link)
            # 链接 star + 1
            link.update(inc__star = 1)
            return True
        except Exception as e:
            app.logger.debug(e)
            return False




@login_manager.user_loader
def load_user( user_id ):
    user = User.objects(id = user_id).first()
    return user
