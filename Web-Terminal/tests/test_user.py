import io
import unittest
from flask import url_for
from flask_login import current_user
from app import db
from app.bundle.accounts.models import User
from tests.base import BaseTestCase


class UserTestCase(BaseTestCase):
    def test_register_user(self):
        """
        Test if user exists and pwd is hashed
        """
        user = User(username='test_user', password='123123')
        db.session.add(user)
        db.session.commit()

        user = User.query.filter_by(username='test_user').first()
        assert user.username == 'test_user'
        assert user.password != '123123'
        
    def test_can_login_user(self):
        """
        Test if user can login
        """
        with self.client:
            response = self.client.post(
                url_for('accounts.login'),
                data=dict(username='test_user', password='123123', remember=True),
                follow_redirects=True
            )
            assert response.status_code == 200

    def test_register_page(self):
        """
        Test if register page loads with 200
        """
        with self.client:
            response = self.client.get(url_for('accounts.register'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'registration', response.data)

    def test_login_page(self):
        """
        Test if the login page loads with a 200
        """
        with self.client:
            response = self.client.get(url_for('accounts.login'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'login', response.data)


if __name__ == "__main__":
    unittest.main()