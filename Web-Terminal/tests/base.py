from flask_testing import TestCase
from app import create_app, db, bcrypt
from app.bundle.accounts.models import User


class BaseTestCase(TestCase):   
    def create_app(self):
        app = create_app('testing')
        return app

    def setUp(self):
        db.create_all()
        user = User(username='admin', password='admin123')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
