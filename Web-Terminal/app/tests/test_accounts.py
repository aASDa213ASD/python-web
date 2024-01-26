from flask_login import current_user

from app import db
from app.bundle.accounts.models import User
from app.tests.conftest import client, init_database, log_in_default_user
from flask import url_for


def test_user_model():
    user = User("user", "password")
    assert user.username == 'user'
    assert user.password != 'password'


def test_register_user(client):
    response = client.post(
        url_for('accounts.register'),
        data=dict(
            username='ross',
            password='123123',
            confirm_password='123123'
        ),
        follow_redirects=True
    )
    assert response.status_code == 200


def test_login_user(client, init_database):
    data = {'username': 'bob', 'password': '123123', 'remember': 'y'}

    response = client.post(
        url_for('accounts.login', external=True),
        data=data,
        follow_redirects=True
    )
    assert response.status_code == 200
    assert current_user.is_authenticated == True


def test_login_user_with_fixture(client, init_database, log_in_default_user):
    assert current_user.is_authenticated == True
  

def test_log_out_user(client, log_in_default_user):
    response = client.get(
        url_for('accounts.exit'),
        follow_redirects=True
    )

    assert response.status_code == 200
    assert current_user.is_authenticated == False