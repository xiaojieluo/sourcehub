from . import StringField, Model, IntField, ListField, DatetimeField
import datetime

class Link(Model):
    '''
    objectid,
    title: 连接标题
    created_at: 记录创建时间
    updated_at: 记录更新时间
    '''
    title = StringField(required = True)
    url = StringField()
    tags = ListField()
    is_show = IntField(default = 1)
    created_at = DatetimeField(default = datetime.datetime.now())
    updated_at = DatetimeField(default = datetime.datetime.now())


    def validate(self, **kw):
        '''
        数据类型验证函数
        '''
    # created_at = DatetimeField(default = datetime.datetime.now())
    # updated_at = DatetimeField(default = datetime.datetime.now())

    # def __init__(self):
    #     self.collection = db[self.__class__.__name__]

    # def save(self):
    #     print(dir(self))
    # def insert(self, *args, **kw):
