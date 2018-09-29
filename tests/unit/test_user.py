from unittest import TestCase
from api.app.models import UserModel


class UserTest(TestCase):
    def test_create_user(self):
        user = UserModel('Test', 'password', False)

        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'Test')
        self.assertEqual(user.password, 'password')

    def test_user_json(self):
        user = UserModel('Test', 'password', False)
        expected = {
            'username': 'Test'
        }
        self.assertDictEqual(user.json(), expected)