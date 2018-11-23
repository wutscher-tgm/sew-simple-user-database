import pytest
import server.main
from flask import url_for
from flask import Flask
import base64


@pytest.yield_fixture(autouse=True)
def run_around_tests():
    file = open('db.json', "w+")
    file.write('[]')


@pytest.fixture
def client():
    server.main.app.testing = True
    client = server.main.app.test_client()
    yield client

def test_get_one_by_email(client):
    client.put('/students?email=rwutscher@student.tgm.ac.at&username=rwutscher')
    res = client.get('/students?email=rwutscher@student.tgm.ac.at')
    assert res.json == {'email': 'rwutscher@student.tgm.ac.at', 'username': 'rwutscher', 'picture': None}


def test_get_one_by_username(client):
    client.put('/students?email=rwutscher@student.tgm.ac.at&username=rwutscher')
    res = client.get('/students?username=rwutscher')
    assert res.json == [{'email': 'rwutscher@student.tgm.ac.at', 'username': 'rwutscher', 'picture': None}]

def test_get_all(client):
    client.put('/students?email=rwutscher@student.tgm.ac.at&username=rwutscher')
    client.put('/students?email=ntesanovic@student.tgm.ac.at&username=ntesanovic')
    res = client.get('/students')
    assert res.json ==  [
        {'email': 'rwutscher@student.tgm.ac.at', 'username': 'rwutscher', 'picture': None},
        {'email': 'ntesanovic@student.tgm.ac.at', 'username': 'ntesanovic', 'picture': None}
    ]
"""
def test_get_one_by_email_with_picture_link(client):
    with open('25224756.jpg', 'rb') as f:
        res = client.put('/students?email=rwutscher@student.tgm.ac.at&username=rwutscher&pictureLink=https://avatars2.githubusercontent.com/u/25224756?s=460&v=4')
        assert res.json == "successful"
        res = client.get('/students?email=rwutscher@student.tgm.ac.at')
        assert res.json == {'email': 'rwutscher@student.tgm.ac.at', 'username': 'rwutscher', 'picture': base64.encodebytes(f.read())}
"""
def test_get_one_by_email_with_picture(client):
    with open('pp.jpg', 'rb') as f:
        res = client.put('/students?email=rwutscher@student.tgm.ac.at&username=rwutscher',data={
            "picture": (f.read(),'')#base64.encodebytes(f.read())
        },content_type='application/x-www-form-urlencoded')
        assert res.json == "successful"
        res = client.get('/students?email=rwutscher@student.tgm.ac.at')
        assert res.json == {'email': 'rwutscher@student.tgm.ac.at', 'username': 'rwutscher', 'picture': base64.encodebytes(f.read())}
"""
def test_get_one_by_username(client):
    client.put('/students?email=rwutscher@student.tgm.ac.at&username=rwutscher')
    res = client.get('/students?username=rwutscher')
    assert res.json == [{'email': 'rwutscher@student.tgm.ac.at', 'username': 'rwutscher', 'picture': None}]

def test_get_all(client):
    client.put('/students?email=rwutscher@student.tgm.ac.at&username=rwutscher')
    client.put('/students?email=ntesanovic@student.tgm.ac.at&username=ntesanovic')
    res = client.get('/students')
    assert res.json ==  [
        {'email': 'rwutscher@student.tgm.ac.at', 'username': 'rwutscher', 'picture': None},
        {'email': 'ntesanovic@student.tgm.ac.at', 'username': 'ntesanovic', 'picture': None}
    ]
"""