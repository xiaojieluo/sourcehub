from mongoengine import Document, StringField, ListField, IntField, DateTimeField, ReferenceField
import datetime
from nav.web import scrapy_title
# from nav import app
from flask import current_app
from nav.models import User
from nav.models.tag import Tag
import threading

class Link(Document):
    title = StringField(default='Unknow')
    url = StringField(required=True)
    tags = ListField(StringField())
    # 是否展示
    is_show = IntField(default=True)
    # 链接投票
    vote = IntField(default=0)
    # 标签被 star 数
    star = IntField(default = 0)
    # 链接被 fork 数
    fork = IntField(default=0)
    # 链接上传者， 内联文档
    author = ReferenceField('User')
    created_at = DateTimeField(default = datetime.datetime.now())
    updated_at = DateTimeField(default = datetime.datetime.now())

    @classmethod
    def insert(cls, form_data):
        '''
        插入数据库
        '''
        t = threading.Thread(target = cls.update_title, name="Threads", args=(cls, form_data['url']))
        t.start()
        data = cls.filter_fields(cls, form_data)
        data['tags'] = cls.handle_tags(cls, data['tags'])
        cls.update_tags(cls, data)

        try:
            link = cls(**data)
            link.save()
            return True
        except Exception as e:
            current_app.logger.debug(e)

    def update_title(self, url):
        '''从 url 中爬取标题， ico等信息， 并更新数据库'''
        link = self.objects(url = url)
        current_app.logger.debug("更新链接标题")
        title = scrapy_title(url)
        data = self.merge_data(self, {'title': title})
        link.update(upsert = True, **data)


    def update_tags(self, data):
        '''根据 data 信息， 更新 tags 表， 向 tags 表中插入必须数据'''
        current_app.logger.info("update tags Document.")
        for tag in data['tags']:
            Tag.update_or_insert(name = tag)
            # tag_model.

    def filter_fields(self, data, exculde = None):
        '''过滤 fields 排除模型中不存在的 field'''
        if exculde is None:
            exculde = ['id']
        fields = [k for k in self._fields.keys() if k not in exculde]
        result =  {k: v for k, v in data.items() if k in fields}

        return result

    def handle_tags(self, tags):
        '''
        处理 tags， 将字符串转换成列表， 两边去掉空格
        '''
        if isinstance(tags, str):
            result = [k.strip() for k in tags.split(',')]
            return result
        else:
            raise TypeError("tags is not str.{}".format(tags))

    def merge_data(self, data):
        '''组装要更新的数据'''
        data.update({
            'updated_at': datetime.datetime.now()
        })
        return data
