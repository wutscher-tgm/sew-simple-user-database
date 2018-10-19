import pytest
import server.main
from flask import url_for
from flask import Flask


@pytest.fixture
def client():
    server.main.app.testing = True
    client = server.main.app.test_client()
    yield client


def test_ping(client):
    res = client.get('/students')
    assert res.status_code == 200
