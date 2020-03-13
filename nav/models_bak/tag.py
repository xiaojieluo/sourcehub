from . import Model, StringField, DatetimeField
import datetime

class Tag(Model):
    '''
    tag model
    '''
    name = StringField()
    created_at = DatetimeField(default = datetime.datetime.now())
    updated_at = DatetimeField(default = datetime.datetime.now())
