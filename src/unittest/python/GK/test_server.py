import pytest
from server.main import create_app
from flask import url_for
import flask.Flask.test_client


@pytest.fixture
def app():
    app = create_app()
    app.debug = True
    return app


def test_ping(client):
    res = client.get(url_for('ping'))
    assert res.status_code == 200
    assert res.json == {'ping': 'pong'}
