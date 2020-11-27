import pytest

def test_index(client):
    response = client.get('/api/')

    # print(response.json)

    assert response.json == {
        'links': 'http://127.0.0.1:5000/api/links', 'users': 'http://127.0.0.1:5000/api/users', 'tags': 'http://127.0.0.1:5000/api/tags'}
