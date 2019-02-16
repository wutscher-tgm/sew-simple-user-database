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

def test_get_one(client):
    client.post('/students', data={
        "email": "rwutscher@student.tgm.ac.at",
        "username": "rwutscher"
    })
    res = client.get('/students?email=rwutscher@student.tgm.ac.at')
    assert res.json == {
        'email': 'rwutscher@student.tgm.ac.at',
        'username': 'rwutscher',
        'picture': None
    }

def test_get_non_existent_user(client):
    client.post('/students', data={
        "email": "rwutscher@student.tgm.ac.at",
        "username": "rwutscher"
    })
    client.post('/students', data={
        "email": "ntesanovic@student.tgm.ac.at",
        "username": "ntesanovic"
    })
    res = client.get('/students?email=pdanho@student.tgm.ac.at')
    assert res.json == "user not found"
    assert res.status_code == 404


def test_get_all(client):
    client.post('/students', data={
        "email": "rwutscher@student.tgm.ac.at",
        "username": "rwutscher"
    })
    client.post('/students', data={
        "email": "ntesanovic@student.tgm.ac.at",
        "username": "ntesanovic"
    })
    res = client.get('/students')
    assert res.json ==  [
        {'email': 'rwutscher@student.tgm.ac.at', 'username': 'rwutscher', 'picture': None},
        {'email': 'ntesanovic@student.tgm.ac.at', 'username': 'ntesanovic', 'picture': None}
    ]

def test_get_one_with_picture_link(client):
    with open('25224756.jpg', 'rb') as f:
        client.post('/students', data={
            "email": "rwutscher@student.tgm.ac.at",
            "username": "rwutscher",
            "pictureLink": "https://avatars2.githubusercontent.com/u/25224756?s=460&v=4"
        })
        res = client.get('/students?email=rwutscher@student.tgm.ac.at')
        assert res.json == {
            'email': 'rwutscher@student.tgm.ac.at',
            'username': 'rwutscher',
            'picture': base64.b64encode(f.read()).decode("utf-8")
        }

def test_get_one_with_picture_file(client):
    with open('pp.jpg', 'rb') as f:
        client.post('/students', data={
            "email": "rwutscher@student.tgm.ac.at",
            "username": "rwutscher",
            "picture": (io.BytesIO(f.read()), 'pp.jpg')
        }, content_type='multipart/form-data')
    res = client.get('/students?email=rwutscher@student.tgm.ac.at')
    with open('pp.jpg', 'rb') as f:
        assert res.json == {
            'email': 'rwutscher@student.tgm.ac.at',
            'username': 'rwutscher',
            'picture': base64.b64encode(f.read()).decode("utf-8")
        }