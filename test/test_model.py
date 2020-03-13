from sourcehub.models import Model, StringField, DatetimeField, IntField
import datetime
import pytest


class User(Model):
    username = StringField()
    created_at = DatetimeField(default = datetime.datetime.now())
    updated_at = DatetimeField(default = datetime.datetime.now())
    age = IntField(default = 18)


@pytest.fixture
def user():
    user = User()
    user.username = 'tests'
    user.insert()
    return user

def test_model_setattr_function():
    user = User()
    user.address = 'china'
    assert user.address == None

def test_model_insert_function():
    result = User.insert(id = 'ignore', username = 'hello')

    from pymongo.results import InsertOneResult
    assert result is not None
    assert type(result) == InsertOneResult


def test_field_default_attrs(user):
    User.insert(username = 'test_field')
    u = User.find({'username': 'test_field'})
    assert u.age == 18

def test_model_find_function():
    User.insert({'username': 'tests'})
    
    result = User.find_all({'username': 'tests'})
    users = [u for u in result]
    assert type(users[0]) == User

    users = User.find({'username': 'no exists'})
    assert users is None
    # print(users)

    # print(list(result))
    # user = User.find({'username': 'tests'})
    # assert user.username == 'tests'
    #
    # user = User.find(username = 'tests')
    # assert user.username == 'tests'
    #
    # user = User.find(id = user.id)
    # assert user.username == 'tests'
    #
    # user = User.find({'id': user.id})
    # assert user.username == 'tests'

def test_model_collection_attrs():
    user = User()
    result = user.collection.insert_one({'fuck': 'fuckss'})
    print(result)


def test_model_save_function():
    # user = User()
    # user.username = 'tests'
    # user.save()
    # assert user.age == 18
    User.insert({'username': 'tests'})
    user = User.find(username = 'tests')

    print(user)
    # user.age = 29
    # user.save()
    # print(user)


# def test_model_metaclass():
#     u = User()
#     u.username = "llnhhy"
#     result = u.insert()
