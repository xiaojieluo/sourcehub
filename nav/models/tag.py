from mongoengine import StringField, Document, DateTimeField, IntField, ReferenceField, ListField
import datetime
# from nav import app
from flask import current_app

class Tag(Document):
    name = StringField(required = True)
    # 标签收藏链接数
    collectNum = IntField(default=0)
    # 标签被 star 数
    star = IntField(default=0)
    # 标签数
    collection = ListField(ReferenceField('Link'))

    created_at = DateTimeField(default = datetime.datetime.now())
    updated_at = DateTimeField(default = datetime.datetime.now())

    @classmethod
    def update_or_insert(cls, **update):
        ''' 更新 tag 表数据，
        插入， 删除， 修改 Link 表时触发此方法。
        当不存在时删除'''
        tag = cls.objects(**update)
        current_app.logger.debug(tag)
        # number = 1
        # if tag.first():
        #     number += tag.collectNum

        # tag.update(upsert=True, **update, collectNum=number)
        tag.update(upsert=True, **update, inc__collectNum =1)

        return tag

    # def collection(self, linkid):
    #     '''将 linkid 加入 tags 中
    #     '''
