import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client


def test_client_invalid_url(client):
    rv = client.get('/url/afcnjof')
    response = rv.get_json()
    assert response['head']['status'] == 'Failed'


def test_client_incomplete_url(client):
    rv = client.get('/url/https://www.bbc.com/')
    response = rv.get_json()
    assert response['head']['status'] == 'Incomplete'


def test_client_complete_url(client):
    rv = client.get('/url/https://www.bbc.com/news')
    response = rv.get_json()
    assert response['head']['status'] == 'Complete'