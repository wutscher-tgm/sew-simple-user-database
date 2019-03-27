import pytest
import server.main
import os
import base64

username='admin@userdb.com'
password='admin'
auth_header = {'Authorization': 'Basic ' + base64.b64encode(bytes(username + ":" + password, 'ascii')).decode('ascii')}

def test_server_creates_db():
    if os.path.exists("db.json"):
        os.remove("db.json")
    server.main.app.testing = True
    client = server.main.app.test_client()
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
