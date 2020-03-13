from pymongo import MongoClient
import datetime

client = MongoClient()
db = client['sourcehub']


class Field(object):
    def __init__(self, *args, **kw):
        self.default = kw.get('default')

    # def __str__(self):
    #     return "<{}:{}>".format(self.__class__.__name__, self.name)

class StringField(Field):
    def __init__(self, default = '', *args, **kw):
        kw.update({
            'default': default
        })
        super(StringField, self).__init__(**kw)


class DatetimeField(Field):
    def __init__(self, default = '', *args, **kw):
        kw.update({
            'default': default
        })
        super(DatetimeField, self).__init__(**kw)
    pass

class IntField(Field):
    def __init__(self, default = '', *args, **kw):
        kw.update({
            'default': default
        })
        super(IntField, self).__init__(**kw)

class

class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        print("Found Model :{}".format(name))
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)

        mappings = {}
        for k, v in attrs.items():
            # print(k)
            # print(isinstance(v, Field))
            if isinstance(v, Field):
                print("Found mapping  {} =====> {}".format(k, v))
                mappings[k] = v

        for k in mappings.keys():
            attrs.pop(k)

        attrs['__mappings__'] = mappings
        attrs['__table__'] = name
        return type.__new__(cls, name, bases, attrs)


class Model(object, metaclass = ModelMetaclass):
    def __init__(self, **kw):
        super(Model, self).__init__(**kw)
        self.collection = db[self.__table__]

    def _get_attrs(self):
        '''
        从模型属性中获取值
        '''
        post = {}
        print(dir(self))
        for key, value in self.__mappings__.items():
            if hasattr(self, key):

                post.update({
                    key: getattr(self, key)
                })
            elif hasattr(value, 'default'):
                post.update({
                    key: value.default
                })
            else:
                pass

        return post

    def find(self, **kw):
        print(dir(self))
        print(self.__mappings__)
        post = {}

        if not kw:
            post.update(self._get_attrs())
        else:
            post.update(kw)
        print(post)

        return self.collection.find_one(post)

    def insert(self, **kw):
        '''向 mongodb 中插入数据
        '''
        post = {}

        if not kw:
            post.update(self._get_attrs())
        else:
            post.update(kw)

        print(post)

        return self.collection.insert_one(post)


class Link(Model):
    '''
    objectid,
    title: 连接标题
    created_at: 记录创建时间
    updated_at: 记录更新时间
    '''
    title = StringField()
    # created_at = DatetimeField(default = datetime.datetime.now())
    # updated_at = DatetimeField(default = datetime.datetime.now())

    def __init__(self):
        self.collection = db[self.__class__.__name__]

    def save(self):
        print(dir(self))
    # def insert(self, *args, **kw):


class User(Model):
    '''
    username
    '''
    def __init__(self):
        # 默认数据表名为类名
        self.collection = db[self.__class__.__name__]
