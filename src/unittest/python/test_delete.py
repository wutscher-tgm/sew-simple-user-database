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
def test_delete_one(client):
    client.post('/', headers=auth_header, data={
        "email": "rwutscher@student.tgm.ac.at",
        "username": "rwutscher"
    })
    client.delete('/', headers=auth_header, data={
        "email": "rwutscher@student.tgm.ac.at"
    })
    res = client.get('/?email=rwutscher@student.tgm.ac.at')
    assert res.json == "user not found"

def test_delete_one_of_many(client):
    client.post('/', headers=auth_header, data={
        "email": "rwutscher@student.tgm.ac.at",
        "username": "rwutscher"
    })
    client.post('/', headers=auth_header, data={
        "email": "ntesanovic@student.tgm.ac.at",
        "username": "ntesanovic"
    })
    client.delete('/', headers=auth_header, data={
        "email": "rwutscher@student.tgm.ac.at"
    })
    res = client.get('/', headers=auth_header)
    assert res.json == [
        {
            "email": "ntesanovic@student.tgm.ac.at",
            "username": "ntesanovic",
            "picture": None
        }
    ]

def test_delete_one_non_existent(client):
    client.delete('/', headers=auth_header, data={
        "email": "rwutscher@student.tgm.ac.at"
    })
    res = client.get('/?email=rwutscher@student.tgm.ac.at', headers=auth_header)
    assert res.json == "user not found"

def test_delete_one_non_existent_of_many(client):
    client.post('/', headers=auth_header, data={
        "email": "rwutscher@student.tgm.ac.at",
        "username": "rwutscher"
    })
    client.post('/', headers=auth_header, data={
        "email": "ntesanovic@student.tgm.ac.at",
        "username": "ntesanovic"
    })
    client.delete('/', headers=auth_header, data={
        "email": "pdanho@student.tgm.ac.at"
    })
    res = client.get('/', headers=auth_header)
    assert res.json == [
        {
            "email": "rwutscher@student.tgm.ac.at",
            "username": "rwutscher",
            "picture": None
        },
        {
            "email": "ntesanovic@student.tgm.ac.at",
            "username": "ntesanovic",
            "picture": None
        }
    ]