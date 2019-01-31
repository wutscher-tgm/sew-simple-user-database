import io

import pytest
import server.main
@pytest.fixture
def client():
    open('db.json', "w+")
    server.main.app.testing = True
    client = server.main.app.test_client()
    yield client


def test_create(client):
    res = client.post('/students', data={
        "email": "rwutscher@student.tgm.ac.at",
        "username": "rwutscher"
    })
    assert res.json == "successful"

def test_create_duplicate(client):
    res = client.post('/students', data={
        "email": "ntesanovic@student.tgm.ac.at",
        "username": "ntesanovic"
    })
    assert res.json == "successful"
    res = client.post('/students', data={
        "email": "ntesanovic@student.tgm.ac.at",
        "username": "ntesanovic"
    })
    assert res.json == "email already exists"

def test_create_with_picture_link(client):
    res = client.post('/students', data={
        "email": "rwutscher@student.tgm.ac.at",
        "username": "rwutscher",
        "pictureLink": "https://avatars2.githubusercontent.com/u/25224756?s=460&v=4"
    })
    assert res.json == "successful"

def test_create_with_picture_file(client):
    with open('pp.jpg', 'rb') as f:
        res = client.post('/students', data={
            "email": "rwutscher@student.tgm.ac.at",
            "username": "rwutscher",
            "picture": (io.BytesIO(f.read()), 'pp.jpg')
        }, content_type='multipart/form-data')
        assert res.json == "successful"