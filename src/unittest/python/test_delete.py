import pytest
import server.main

@pytest.fixture
def client():
    open('db.json', "w+")
    server.main.app.testing = True
    client = server.main.app.test_client()
    yield client

def test_delete_one(client):
    client.post('/students', data={
        "email": "rwutscher@student.tgm.ac.at",
        "username": "rwutscher"
    })
    client.delete('/students', data={
        "email": "rwutscher@student.tgm.ac.at"
    })
    res = client.get('/students?email=rwutscher@student.tgm.ac.at')
    assert res.json == "user not found"

def test_delete_one_of_many(client):
    client.post('/students', data={
        "email": "rwutscher@student.tgm.ac.at",
        "username": "rwutscher"
    })
    client.post('/students', data={
        "email": "ntesanovic@student.tgm.ac.at",
        "username": "ntesanovic"
    })
    client.delete('/students', data={
        "email": "rwutscher@student.tgm.ac.at"
    })
    res = client.get('/students')
    assert res.json == [
        {
            "email": "ntesanovic@student.tgm.ac.at",
            "username": "ntesanovic",
            "picture": None
        }
    ]

def test_delete_one_non_existent(client):
    client.delete('/students', data={
        "email": "rwutscher@student.tgm.ac.at"
    })
    res = client.get('/students?email=rwutscher@student.tgm.ac.at')
    assert res.json == "user not found"

def test_delete_one_non_existent_of_many(client):
    client.post('/students', data={
        "email": "rwutscher@student.tgm.ac.at",
        "username": "rwutscher"
    })
    client.post('/students', data={
        "email": "ntesanovic@student.tgm.ac.at",
        "username": "ntesanovic"
    })
    client.delete('/students', data={
        "email": "pdanho@student.tgm.ac.at"
    })
    res = client.get('/students')
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