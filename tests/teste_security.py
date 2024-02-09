from jose import jwt

from fast_hero.security import SECRET_KEY, create_access_token


def test_jwt():
    data = {'teste': 'test'}
    token = create_access_token(data)

    decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

    assert decoded['test'] == data['teste']
    assert decoded['exp']
