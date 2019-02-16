import pytest
import server.main
import os

def test_server_creates_db():
    if os.path.exists("db.json"):
        os.remove("db.json")
    server.main.app.testing = True
    client = server.main.app.test_client()
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
