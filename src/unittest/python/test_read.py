import io
import pytest
import server.main
import base64

@pytest.fixture
def client():
    open('db.json', "w+")
    server.main.app.testing = True
    client = server.main.app.test_client()
    yield client

username='admin@userdb.com'
password='admin'
auth_header = {'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')}
def test_get_one(client):
    client.post('/', headers=auth_header, data={
        "email": "rwutscher@student.tgm.ac.at",
        "username": "rwutscher"
    })
    res = client.get('/?email=rwutscher@student.tgm.ac.at', headers=auth_header)
    assert res.json == {
        'email': 'rwutscher@student.tgm.ac.at',
        'username': 'rwutscher',
        'picture': None
    }

def test_get_non_existent_user(client):
    client.post('/', headers=auth_header, data={
        "email": "rwutscher@student.tgm.ac.at",
        "username": "rwutscher"
    })
    client.post('/', headers=auth_header, data={
        "email": "ntesanovic@student.tgm.ac.at",
        "username": "ntesanovic"
    })
    res = client.get('/?email=pdanho@student.tgm.ac.at', headers=auth_header)
    assert res.json == "user not found"
    assert res.status_code == 404


def test_get_all(client):
    client.post('/', headers=auth_header, data={
        "email": "rwutscher@student.tgm.ac.at",
        "username": "rwutscher"
    })
    client.post('/', headers=auth_header, data={
        "email": "ntesanovic@student.tgm.ac.at",
        "username": "ntesanovic"
    })
    res = client.get('/', headers=auth_header)
    assert res.json ==  [
        {'email': 'rwutscher@student.tgm.ac.at', 'username': 'rwutscher', 'picture': None},
        {'email': 'ntesanovic@student.tgm.ac.at', 'username': 'ntesanovic', 'picture': None}
    ]

def test_get_one_with_picture_link(client):
    with open('25224756.jpg', 'rb') as f:
        client.post('/', headers=auth_header, data={
            "email": "rwutscher@student.tgm.ac.at",
            "username": "rwutscher",
            "pictureLink": "https://avatars2.githubusercontent.com/u/25224756?s=460&v=4"
        })
        res = client.get('/?email=rwutscher@student.tgm.ac.at', headers=auth_header)
        assert res.json == {
            'email': 'rwutscher@student.tgm.ac.at',
            'username': 'rwutscher',
            'picture': base64.b64encode(f.read()).decode("utf-8")
        }

def test_get_one_with_picture_file(client):
    with open('pp.jpg', 'rb') as f:
        client.post('/', headers=auth_header, data={
            "email": "rwutscher@student.tgm.ac.at",
            "username": "rwutscher",
            "picture": (io.BytesIO(f.read()), 'pp.jpg')
        }, content_type='multipart/form-data')
    res = client.get('/?email=rwutscher@student.tgm.ac.at', headers=auth_header)
    with open('pp.jpg', 'rb') as f:
        assert res.json == {
            'email': 'rwutscher@student.tgm.ac.at',
            'username': 'rwutscher',
            'picture': base64.b64encode(f.read()).decode("utf-8")
        }