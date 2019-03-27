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
def test_update_username_status(client):
    res = client.post('/', headers=auth_header, data={
        "email": "rwutscher@student.tgm.ac.at",
        "username": "rwutscher"
    })
    assert res.status_code == 200
    res = client.patch('/', headers=auth_header, data={
        "email": "rwutscher@student.tgm.ac.at",
        "username": "rwutscher2"
    })
    assert res.status_code == 200
    res = client.get('/?email=rwutscher@student.tgm.ac.at', headers=auth_header)
    assert res.status_code == 200

def test_update_username_content(client):
    client.post('/', headers=auth_header, data={
        "email": "rwutscher@student.tgm.ac.at",
        "username": "rwutscher"
    })
    client.patch('/', headers=auth_header, data={
        "email": "rwutscher@student.tgm.ac.at",
        "username": "rwutscher2"
    })
    res = client.get('/?email=rwutscher@student.tgm.ac.at', headers=auth_header)
    assert res.json == {
        "email": "rwutscher@student.tgm.ac.at",
        "username": "rwutscher2",
        "picture": None
    }

def test_update_non_existent_user_status(client):
    res = client.post('/', headers=auth_header, data={
        "email": "rwutscher@student.tgm.ac.at",
        "username": "rwutscher"
    })
    assert res.status_code == 200
    res = client.post('/', headers=auth_header, data={
        "email": "ntesanovic@student.tgm.ac.at",
        "username": "ntesanovic"
    })
    assert res.status_code == 200
    res = client.patch('/', headers=auth_header, data={
        "email": "pdanho@student.tgm.ac.at",
        "username": "pdanho3"
    })
    assert res.status_code == 404

def test_update_non_existent_user_content(client):
    client.post('/', headers=auth_header, data={
        "email": "rwutscher@student.tgm.ac.at",
        "username": "rwutscher"
    })
    client.post('/', headers=auth_header, data={
        "email": "ntesanovic@student.tgm.ac.at",
        "username": "ntesanovic"
    })
    res = client.patch('/', headers=auth_header, data={
        "email": "pdanho@student.tgm.ac.at",
        "username": "pdanho3"
    })
    assert res.json == "user not found"

def test_update_picture_link_status(client):
    res = client.post('/', headers=auth_header, data={
        "email": "rwutscher@student.tgm.ac.at",
        "username": "rwutscher",
        "pictureLink": None
    })
    assert res.status_code == 200
    res = client.patch('/', headers=auth_header, data={
        "email": "rwutscher@student.tgm.ac.at",
        "pictureLink": "https://avatars2.githubusercontent.com/u/25224756?s=460&v=4"
    })
    assert res.status_code == 200
    res = client.get('/?email=rwutscher@student.tgm.ac.at', headers=auth_header)
    assert res.status_code == 200

def test_update_picture_link_content(client):
    with open('25224756.jpg', 'rb') as f:
        client.post('/', headers=auth_header, data={
            "email": "rwutscher@student.tgm.ac.at",
            "username": "rwutscher",
            "pictureLink": None
        })
        client.patch('/', headers=auth_header, data={
            "email": "rwutscher@student.tgm.ac.at",
            "pictureLink": "https://avatars2.githubusercontent.com/u/25224756?s=460&v=4"
        })
        res = client.get('/?email=rwutscher@student.tgm.ac.at', headers=auth_header)
        assert res.json == {
            'email': 'rwutscher@student.tgm.ac.at',
            'username': 'rwutscher',
            'picture': base64.b64encode(f.read()).decode("utf-8")
        }

def test_update_picture_file_status(client):
    res = client.post('/', headers=auth_header, data={
        "email": "rwutscher@student.tgm.ac.at",
        "username": "rwutscher"
    })
    assert res.status_code == 200
    with open('pp.jpg', 'rb') as f:
        res = client.patch('/', headers=auth_header, data={
            "email": "rwutscher@student.tgm.ac.at",
            "picture": (io.BytesIO(f.read()), 'pp.jpg')
        }, content_type='multipart/form-data')
        assert res.status_code == 200
    res = client.get('/?email=rwutscher@student.tgm.ac.at', headers=auth_header)
    assert res.status_code == 200

def test_update_picture_file_content(client):
    client.post('/', headers=auth_header, data={
        "email": "rwutscher@student.tgm.ac.at",
        "username": "rwutscher"
    })
    with open('pp.jpg', 'rb') as f:
        client.patch('/', headers=auth_header, data={
            "email": "rwutscher@student.tgm.ac.at",
            "picture": (io.BytesIO(f.read()), 'pp.jpg')
        }, content_type='multipart/form-data')
    res = client.get('/?email=rwutscher@student.tgm.ac.at', headers=auth_header)
    with open('pp.jpg', 'rb') as f:
        assert res.json == {
            'email': 'rwutscher@student.tgm.ac.at',
            'username': 'rwutscher',
            'picture': base64.b64encode(f.read()).decode("utf-8")
        }

def test_update_picture_link_and_username_status(client):
    res = client.post('/', headers=auth_header, data={
        "email": "rwutscher@student.tgm.ac.at",
        "username": "rwutscher",
        "pictureLink": None
    })
    assert res.status_code == 200
    res = client.patch('/', headers=auth_header, data={
        "email": "rwutscher@student.tgm.ac.at",
        "pictureLink": "https://avatars2.githubusercontent.com/u/25224756?s=460&v=4",
        "username": "rwutscher2"
    })
    assert res.status_code == 200
    res = client.get('/?email=rwutscher@student.tgm.ac.at', headers=auth_header)
    assert res.status_code == 200

def test_update_picture_link_and_username_content(client):
    with open('25224756.jpg', 'rb') as f:
        client.post('/', headers=auth_header, data={
            "email": "rwutscher@student.tgm.ac.at",
            "username": "rwutscher",
            "pictureLink": None
        })
        client.patch('/', headers=auth_header, data={
            "email": "rwutscher@student.tgm.ac.at",
            "pictureLink": "https://avatars2.githubusercontent.com/u/25224756?s=460&v=4",
            "username": "rwutscher2"
        })
        res = client.get('/?email=rwutscher@student.tgm.ac.at', headers=auth_header)
        assert res.json == {
            'email': 'rwutscher@student.tgm.ac.at',
            'username': 'rwutscher2',
            'picture': base64.b64encode(f.read()).decode("utf-8"),
        }

def test_update_picture_file_and_username_status(client):
    res = client.post('/', headers=auth_header, data={
        "email": "rwutscher@student.tgm.ac.at",
        "username": "rwutscher"
    })
    assert res.status_code == 200
    with open('pp.jpg', 'rb') as f:
        res = client.patch('/', headers=auth_header, data={
            "email": "rwutscher@student.tgm.ac.at",
            "picture": (io.BytesIO(f.read()), 'pp.jpg'),
            "username": "rwutscher2"
        }, content_type='multipart/form-data')
        assert res.status_code == 200
    res = client.get('/?email=rwutscher@student.tgm.ac.at', headers=auth_header)
    assert res.status_code == 200

def test_update_picture_file_and_username_content(client):
    client.post('/', headers=auth_header, data={
        "email": "rwutscher@student.tgm.ac.at",
        "username": "rwutscher"
    })
    with open('pp.jpg', 'rb') as f:
        client.patch('/', headers=auth_header, data={
            "email": "rwutscher@student.tgm.ac.at",
            "picture": (io.BytesIO(f.read()), 'pp.jpg'),
            "username": "rwutscher2"
        }, content_type='multipart/form-data')
    res = client.get('/?email=rwutscher@student.tgm.ac.at', headers=auth_header)
    with open('pp.jpg', 'rb') as f:
        assert res.json == {
            'email': 'rwutscher@student.tgm.ac.at',
            'username': 'rwutscher2',
            'picture': base64.b64encode(f.read()).decode("utf-8")
        }

def test_update_without_email_status(client):
    res = client.post('/', headers=auth_header, data={
        "email": "rwutscher@student.tgm.ac.at",
        "username": "rwutscher"
    })
    assert res.status_code == 200
    res = client.patch('/', headers=auth_header, data={
        "username": "rwutscher"
    })
    assert res.status_code == 404

def test_update_without_email_content(client):
    client.post('/', headers=auth_header, data={
        "email": "rwutscher@student.tgm.ac.at",
        "username": "rwutscher"
    })
    res = client.patch('/', headers=auth_header, data={
        "username": "rwutscher"
    })
    assert res.json == 'argument "email" is missing'

def test_update_with_picture_file_and_link_status(client):
    res = client.post('/', headers=auth_header, data={
        "email": "rwutscher@student.tgm.ac.at",
        "username": "rwutscher"
    })
    assert res.status_code == 200
    with open('pp.jpg', 'rb') as f:
        res = client.patch('/', headers=auth_header, data={
            "email": "rwutscher@student.tgm.ac.at",
            "picture": (io.BytesIO(f.read()), 'pp.jpg'),
            "pictureLink": "https://avatars2.githubusercontent.com/u/25224756?s=460&v=4"
        }, content_type='multipart/form-data')
        assert res.status_code == 500

def test_update_with_picture_file_and_link_content(client):
    client.post('/', headers=auth_header, data={
        "email": "rwutscher@student.tgm.ac.at",
        "username": "rwutscher"
    })
    with open('pp.jpg', 'rb') as f:
        res = client.patch('/', headers=auth_header, data={
            "email": "rwutscher@student.tgm.ac.at",
            "picture": (io.BytesIO(f.read()), 'pp.jpg'),
            "pictureLink": "https://avatars2.githubusercontent.com/u/25224756?s=460&v=4"
        }, content_type='multipart/form-data')
        assert res.json == 'too many arguments provided, can only use one picture source'

def test_update_with_picture_file_and_link_and_username_status(client):
    res = client.post('/', headers=auth_header, data={
        "email": "rwutscher@student.tgm.ac.at",
        "username": "rwutscher"
    })
    assert res.status_code == 200
    with open('pp.jpg', 'rb') as f:
        res = client.patch('/', headers=auth_header, data={
            "email": "rwutscher@student.tgm.ac.at",
            "picture": (io.BytesIO(f.read()), 'pp.jpg'),
            "pictureLink": "https://avatars2.githubusercontent.com/u/25224756?s=460&v=4",
            "username": "rwutscher2"
        }, content_type='multipart/form-data')
        assert res.status_code == 500

def test_update_with_picture_file_and_link_and_username_content(client):
    client.post('/', headers=auth_header, data={
        "email": "rwutscher@student.tgm.ac.at",
        "username": "rwutscher"
    })
    with open('pp.jpg', 'rb') as f:
        res = client.patch('/', headers=auth_header, data={
            "email": "rwutscher@student.tgm.ac.at",
            "picture": (io.BytesIO(f.read()), 'pp.jpg'),
            "pictureLink": "https://avatars2.githubusercontent.com/u/25224756?s=460&v=4",
            "username": "rwutscher2"
        }, content_type='multipart/form-data')
        assert res.json == 'too many arguments provided, can only use one picture source'