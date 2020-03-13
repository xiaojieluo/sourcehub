class FieldValidateError(Exception):
    '''Field 验证异常'''
    pass


class Field(object):
    def __init__(self, *args, **kw):
        self.default = kw.get('default')

    def validate(self, attrs):
        pass

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

class IntField(Field):
    '''整数类型
    '''
    def __init__(self, default = '', *args, **kw):
        kw.update({
            'default': default
        })
        super(IntField, self).__init__(**kw)

    def validate(self, attrs):
        if not isinstance(attrs, int):
            raise FieldValidateError("{}:{} is not int".format(attrs, type(attrs)))

class ListField(Field):
    '''
    列表
    '''
    def __init__(self, default = None, *args, **kw):
        print(args)
        print(kw)
        if default is None:
            default = []
        kw.update({
            'default': default
        })
        super(ListField, self).__init__(**kw)

    def validate(self, attrs):
        '''Field 验证'''
        if not isinstance(attrs, list):
            # raise FieldValidateError("{} type is not list".format(attrs))
            raise FieldValidateError("{}:{} is not list".format(attrs, type(attrs)))
