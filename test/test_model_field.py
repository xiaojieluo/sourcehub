# import pytest
from nav.models import Model, StringField, ListField, FieldValidateError

class Case(Model):
    tags = ListField()

def test_ListField():
    test = Case()

    Case.insert(tags = ['hello', 'world'])

    try:
        test.tags = 'hello'
    except FieldValidateError as e:
        pass
