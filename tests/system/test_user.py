from api.app.models import UserModel
from tests.base_test import BaseTest
import json


class UserTest(BaseTest):
    def test_register_user(self):
        response = self.client.post('/register',
                                    data=json.dumps({'username': 'test',
                                                     'password': 'password'}),
                                    headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(UserModel.find_by_username('test'))
        expected = {"message": "User 'test' created successfully."}
        self.assertDictEqual(expected, json.loads(response.data))

    def test_register_and_login(self):
        UserModel('test', 'password', True).save_to_db()
        auth_response = self.client.post('/login',
                                         data=json.dumps({'username': 'test', 'password': 'password'}),
                                         headers={'Content-Type': 'application/json'})
        self.assertIn('access_token', json.loads(auth_response.data).keys())

    def test_register_duplicate_user(self):
        user = UserModel('test', 'password', True)
        user.save_to_db()
        response = self.client.post('/register',
                                    data=json.dumps({'username': 'test', 'password': 'password'}),
                                    headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 400)
        expected = {"message": "A user with that username already exists"}
        self.assertDictEqual(expected, json.loads(response.data))
