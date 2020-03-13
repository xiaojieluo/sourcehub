from pymongo import MongoClient
import datetime
from . import Field

client = MongoClient()
db = client['nav']

# debug = True

def dump(msg, *attrs, debug = False, **kw):
    if debug:
        print(msg.format(*attrs, **kw))

'''
此类只是 pymongo 的代理类， 具体使用 API 参考 https://api.mongodb.com/python/current/
'''
class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        # print("Found Model: {}".format(name))
        dump("Found Model: {}", name)
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        mappings = {}
        for k, v in attrs.items():
            if isinstance(v, Field):
                dump("Found mapping {} ===> {}", k, v)
                mappings[k] = v

        for k in mappings.keys():
            attrs.pop(k)

        attrs['__mappings__'] = mappings
        attrs['__table__'] = name
        attrs['collection'] = db[name]
        return type.__new__(cls, name, bases, attrs)


class Model(object, metaclass = ModelMetaclass):
    '''
    模型类
    为用户提供易用的 pymongo API

    若此类现有的 API 无法满足需求， 可以操作 self.collection 来实现越过代理， 直接使用 pymongo 的 API
    !! 请确保在熟知 pymongo API 的情况下再做此操作。
    Example:
        user = User()
        user.collection.insert_one({'username': 'tests'})

    '''
    def __init__(self, *args, **kw):
        # print(self.__class__.__name__)
        self.collection = db[self.__class__.__name__]
        for key, value in kw.items():
            if key == '_id':
                self.__dict__['id'] = value
            else:
                self.__dict__[key] = value

    def __setattr__(self, key, value):
        '''
        设置对象字段值
        一般情况下， id 值不允许修改
        '''
        dump("======= setattr =======")
        if key == 'id':
            raise TypeError("id attribute cannot modify")
        if key in self.__mappings__:
            self.field_validate(key, value)
            self.__dict__[key] = value

    def field_validate(self, field, value):
        ''' field 类型验证函数
        '''
        self.__mappings__[field].validate(value)

    def __getattr__(self, key):
        if key in self.__mappings__:
            if key in self.__dict__:
                return self.__dict__[key]
            else:
                return getattr(self.__mappings__[key], 'default')

    def _get_attrs(self, **kw):
        post = {}
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
        post.update(kw)
        return post

    @classmethod
    def find_all(cls, filter,  **kw):
        '''
        查询所有匹配的数据， 返回生成器格式
        '''
        if 'id' in filter:
            filter['_id'] = kw['id']
            filter.pop('id')

        result = cls.collection.find(filter, **kw)
        for key in result:
            yield cls(**key)

    @classmethod
    def find(cls, filter,  **kw):
        '''
        查询一条匹配的数据， 返回模型实例
        '''
        if 'id' in filter:
            filter['_id'] = filter['id']
            filter.pop('id')

        result = cls.collection.find_one(filter, **kw)
        if result:
            return cls(**result)

    @classmethod
    def insert(cls, *args, **kw):
        '''
        向数据库中插入数据， 返回 pymongo.results.InsertOneResult
        具体 API 用法查阅 pymongo:
        https://api.mongodb.com/python/current/api/pymongo/results.html#pymongo.results.InsertOneResult
        '''
        dump("=== insert ===")

        condition = cls._get_attrs(cls)
        for key in args:
            if isinstance(key, dict):
                for k, v in key.items():
                    if k in cls.__mappings__:
                        condition.update(key)
                # if key in cls.__mappings__:
                #     condition.update(key)

        for k, v in kw.items():
            if k in cls.__mappings__:
                # dump(cls.__mappings__[k])
                cls.__mappings__[k].validate(v)
                # print(dir(cls.__mappings__[k]))
                # print(v)
                # print(k)
                # print(cls.__mappings__[k].validate(v))
                condition.update({k:v})

        # print(condition)
        return cls.collection.insert_one(condition)

    def save(self):
        '''
        保存当前对象到数据库
        分两种模式：
            1. 如果 self.id 存在，则表示是从数据库中取出的， 就根据 self.id 更新数据库。
            2. 如果 self.id 不存在， 则直接将当前对象的字段值存入数据库中。
        '''
        dump(self.id)
        dump(self.__dict__)
        if self.id is None:
            self.insert(**self.__dict__)
        else:
            id = self.id
            self.__dict__.pop('id')
            self.update({'_id': id}, self.__dict__)

    def update(self, filter, update, many = False, **kw):
        '''
        update 接口用法和 pymongo 的 update_one 大致一致， 不同之处在下面列出

        many: boolean | default = False
            当 many 为 True 时，更新所有查询到的数据，
            当 many 为 False 时, 只更新一条数据

        其余具体 API 请查阅：
        https://api.mongodb.com/python/current/api/pymongo/collection.html#pymongo.collection.Collection.update_one
        '''
        print("==== update ====")
        result = self.collection.update_one(filter, {'$set': update}, **kw)
        return result
        # if hasattr(self, id)

    # def save(self):
    #     ''' 保存当前对象的数据到 Mongodb
    #     当数据不存在时新建，当数据存在时替换更新
    #     '''
    #     post = {}
    #     post.update(self._get_attrs())
    #
    #     print(post)
