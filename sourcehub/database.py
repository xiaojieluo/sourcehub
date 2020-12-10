from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import class_mapper
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class MutableList(Mutable, list):

    def __setitem__(self, key, value):
        list.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):
        list.__delitem__(self, key)
        self.changed()

    def append(self, value):
        list.append(self, value)
        self.changed()

    def pop(self, index=0):
        value = list.pop(self, index)
        self.changed()
        return value

    def remove(self, item):
        list.remove(self, item)
        self.changed()

    def clear(self):
        list.clear(self)
        self.changed()

    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, MutableList):
            if isinstance(value, list):
                return MutableList(value)
            return Mutable.coerce(key, value)
        else:
            return value

class ModelMixin(object):

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

        return out