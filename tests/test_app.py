import pytest
from fastapi.testclient import TestClient

from fast_hero.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_root_return_200(client):
    response = client.get('/')

    assert response.status_code == 200
    assert response.json() == {'message': 'Olá Mundo!'}


def test_hello_page_return_text(client):
    response = client.get('/hello')
    assert response.status_code == 200

    expected_html = '<html><head><title>Olá Mundo</title></head><body><h1>Olá Mundo</h1></body></html>'

    assert response.text == expected_html


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'Alice',
            'email': 'alice@mail.com',
            'password': 'secret',
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        'username': 'Alice',
        'email': 'alice@mail.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == 200

    assert response.json() == {
        'users': [{'username': 'Alice', 'email': 'alice@mail.com', 'id': 1}]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'John Doe',
            'email': 'jhon@mail.com',
            'password': 'setpassword',
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        'username': 'John Doe',
        'email': 'jhon@mail.com',
        'id': 1,
    }


def test_user_delete(client):
    response = client.delete('/users/1')

    assert response.status_code == 200
    assert response.json() == {'message': 'User delete!!'}
