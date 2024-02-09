def test_root_return_200(client):
    response = client.get('/')

    assert response.status_code == 200
    assert response.json() == {'message': 'Olá Mundo!'}


def test_hello_page_return_text(client):
    response = client.get('/hello')
    assert response.status_code == 200

    expected_html = '<html><head><title>Olá Mundo</title></head><body><h1>Olá Mundo</h1></body></html>'

    assert response.text == expected_html
