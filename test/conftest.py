import os
import sys

import pytest
from sourcehub import make_app
from sourcehub import db

@pytest.fixture
def app():
    app = make_app()
    app.config['TESTING'] = True

    return app

@pytest.fixture
def client(app):
    """返回 flask 内置的测试客户端

    Args:
        app ([type]): [description]

    Returns:
        [type]: [description]
    """
    return app.test_client()