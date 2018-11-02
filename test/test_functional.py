import pytest
from flask import json

import sys
sys.path.append("..")

from ..app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False
    client = app.test_client()
    yield client


def test_client_invalid_url(client):
    response = client.get('/info?url=afcnjof')
    response = json.loads(response.data)
    assert response['header']['status'] == 'Failed'


def test_client_incomplete_url(client):
    response = client.get('/info?url=https://www.bbc.com/')
    response = json.loads(response.data)
    assert response['header']['status'] == 'Incomplete'


def test_client_complete_url(client):
    response = client.get('/info?url=https://www.bbc.com/news')
    response = json.loads(response.data)
    assert response['header']['status'] == 'Complete'