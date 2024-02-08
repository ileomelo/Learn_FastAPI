from jose import jwt

from fast_hero.security import SECRET_KEY, create_access_token


def test_jwt():
    data = {'teste': 'test'}
    token = create_access_token(data)

    decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

    assert decoded['test'] == data['teste']
    assert decoded['exp']


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == 200
    assert 'access_token' in token
    assert 'token_type' in token
