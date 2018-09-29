from unittest import TestCase
from api.app import create_app, db
from api.app.models import DriverModel, TeamModel


class BaseTest(TestCase):
    def setUp(self):
        self.app = create_app('testing')
        with self.app.app_context():
            db.create_all()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()