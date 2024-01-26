from flask import url_for
from app.tests.conftest import client, init_database, log_in_default_user

def test_register_page(client):
    response = client.get(url_for('accounts.register'))
    assert response.status_code == 200
    assert b'Welcome' in response.data


def test_login_page(client):
    response = client.get(url_for('accounts.login'))
    assert response.status_code == 200
    assert b'Welcome' in response.data


def test_users_page(client, init_database, log_in_default_user):
    response = client.get(url_for('accounts.users', id=1))
    print(response.data)
    assert response.status_code == 200
    assert b'next list' in response.data
