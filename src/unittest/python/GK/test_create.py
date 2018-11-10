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


def test_create(client):
    res = client.put('/students?email=rwutscher@student.tgm.ac.at&username=rwutscher')
    assert res.json == "successful"

def test_create_duplicate(client):
    res = client.put('/students?email=ntesanovic@student.tgm.ac.at&username=ntesanovic')
    assert res.json == "successful"
    res = client.put('/students?email=ntesanovic@student.tgm.ac.at&username=ntesanovic')
    assert res.json == "email already exists"

def test_create_with_picture_link(client):
    res = client.put('/students?email=rwutscher@student.tgm.ac.at&username=rwutscher&pictureLink=https://avatars2.githubusercontent.com/u/25224756?s=460&v=4')
    assert res.json == "successful"

def test_create_with_picture(client):
    with open('pp.jpg', 'rb') as f:
        res = client.put('/students?email=rwutscher@student.tgm.ac.at&username=rwutscher',data={
            "picture": base64.encodebytes(f.read())
        })
        assert res.json == "successful"