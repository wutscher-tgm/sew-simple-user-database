import io

import pytest
import server.main
@pytest.fixture
def client():
    open('db.json', "w+")
    server.main.app.testing = True
    
    client = server.main.app.test_client()
    yield client



def generate_header(client,method,link):
    response2 = None
    if method == 'POST':
        response2 = client.post(link)
    if method == 'PUT':
        response2 = client.put(link)
    if method == 'DELETE':
        response2 = client.delete(link)
    if method == 'GET':
        response2 = client.get(link)
    header = response2.headers.get('WWW-Authenticate')
    auth_type, auth_info = header.split(None, 1)
    d = parse_dict_header(auth_info)
    a1 = 'admin:' + d['realm'] + ':admin'
    realm = d['realm']
    ha1 = md5(a1).hexdigest()
    a2 = '%s:%s' % (method, link)
    ha2 = md5(a2).hexdigest()
    a3 = ha1 + ':' + d['nonce'] + ':' + ha2
    auth_response = md5(a3).hexdigest()
    header = {
            'Authorization': 'Digest username="admin",realm="{0}",'
                             'nonce="{1}",uri="{2}",response="{3}",'
                             'opaque="{4}"'.format(d['realm'],
                                                   d['nonce'],
                                                   link,
                                                   auth_response,
                                                   d['opaque']
                                                   )}
    return header



def test_create(client):
    res = client.post('/students', data={
        "email": "rwutscher@student.tgm.ac.at",
        "username": "rwutscher"
    })
    assert res.json == "successful"

def test_create_without_email(client):
    res = client.post('/students', data={
        "username": "rwutscher"
    })
    assert res.json == 'argument "email" is missing'

def test_create_without_username(client):
    res = client.post('/students', data={
        "email": "rwutscher@student.tgm.ac.at",
    })
    assert res.json == 'argument "username" is missing'

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

def test_create_with_picture_link_and_file(client):
    with open('pp.jpg', 'rb') as f:
        res = client.post('/students', data={
            "email": "rwutscher@student.tgm.ac.at",
            "username": "rwutscher",
            "pictureLink": "https://avatars2.githubusercontent.com/u/25224756?s=460&v=4",
            "picture": (io.BytesIO(f.read()), 'pp.jpg')
        }, content_type='multipart/form-data')
        assert res.json == "too many arguments provided, can only use one picture source"

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