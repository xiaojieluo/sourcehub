from wtforms.validators import ValidationError
from bs4 import BeautifulSoup

import requests
from flask import current_app

class Unique(object):
    def __init__(self, model, field, message = "该内容已存在."):
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field):
        check = self.model.objects(self.field == field.data).first()
        if check is not None and check.url == field.data:
            raise ValidationError(self.message)

def scrapy_title(url):
    '''
    抓取网页标题
    '''
    try:
        res = requests.get(url, timeout=3)
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup.title.string
    except Exception as e:
        current_app.logger.debug(e)
        return 'Unknow'
