from app                        import db
from app.bundle.accounts.models import User
from app.tests.conftest         import client, init_database, log_in_default_user


from flask                      import url_for
from flask_login                import current_user


def test_user_model():
    user = User("user", "password")
    # Check if user model is created
    assert user.username == 'user'
    # Check if password has been hashed
    assert user.password != 'password'


def test_user_login(client):
    response = client.post(
        url_for('accounts.register'),
        data=dict(
            username='registered',
            password='123123',
            confirmation_password='123123'
        ),
        follow_redirects=True
    )
    assert response.status_code == 200


def test_user_register(client, init_database):
    response = client.post(
        url_for('accounts.login', external=True),
        data=dict(
            username='patkennedy',
            password='123123123',
            remember = True
        ),
        follow_redirects=True
    )

    assert response.status_code == 200
    assert current_user.is_authenticated() == True

def test_user_fixture(client, init_database, log_in_default_user):
    assert current_user.is_authenticated() == True
  

def test_user_logout(client, log_in_default_user):
    response = client.get(
        url_for('accounts.exit'),
        follow_redirects=True
    )

    assert response.status_code == 200
    assert current_user.is_authenticated == False