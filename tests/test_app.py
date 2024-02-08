from fast_hero.schemas import UserPublic


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
    response = client.get('/users')

    assert response.status_code == 200

    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_user_delete(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 200
    assert response.json() == {'message': 'User deleted'}
