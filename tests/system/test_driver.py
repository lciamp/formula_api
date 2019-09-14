import json
from datetime import date
from api.app.models import DriverModel, UserModel
from tests.base_test import BaseTest


class DriverTest(BaseTest):
    def setUp(self):
        super(DriverTest, self).setUp()
        UserModel('test', 'password', True).save_to_db()
        auth_response = self.client.post('/login',
                                         data=json.dumps({'username': 'test', 'password': 'password'}),
                                         headers={'Content-Type': 'application/json'})
        self.token = 'Bearer {}'.format(json.loads(auth_response.data).get('access_token'))

    def test_get_driver_with_auth(self):
        headers = {'Authorization': self.token}
        DriverModel('test fn', 'test ln', 0, 1, 'test', 0, 0, 0, date(1995, 8, 25)).save_to_db()

        response = self.client.get('/drivers/1', headers=headers)
        self.assertEqual(response.status_code, 200)

        expected = {
            'id': 1,
            'first_name': 'test fn',
            'last_name': 'test ln',
            'number': 0,
            'team':
                {'base': None,
                 'car': None,
                 'championships': 0,
                 'chief': None,
                 'id': 0,
                 'name': None,
                 'power_unit': None,
                 'since': None},
            'country': 'test',
            'podiums': 0,
            'points': 0,
            'championships': 0,
            'birthday': 'Fri, 25 Aug 1995 00:00:00 -0000',
        }

        self.assertDictEqual(expected, json.loads(response.data))

    def test_get_driver_no_auth(self):
        DriverModel('test fn', 'test ln', 0, 1, 'test', 0, 0, 0, date(1995, 8, 25)).save_to_db()
        response = self.client.get('/drivers/1')
        self.assertEqual(response.status_code, 200)

        expected = {
            "first_name": "test fn",
            "last_name": "test ln",
            "number": 0,
            "message": "more information if logged in."
        }

        self.assertDictEqual(expected, json.loads(response.data))

    def test_driver_not_found(self):
        response = self.client.get('/drivers/1')
        self.assertEqual(response.status_code, 404)
        expected = {"message": "DriverId '1' not found"}
        self.assertDictEqual(expected, json.loads(response.data))

    def test_delete_driver(self):
        DriverModel('test fn', 'test ln', 0, 1, 'test', 0, 0, 0, date(1995, 8, 25)).save_to_db()
        headers = {'Authorization': self.token}
        response = self.client.delete('/drivers/1', headers=headers)

        self.assertEqual(response.status_code, 202)

        self.assertDictEqual({'message': "DriverId: 1 deleted."}, json.loads(response.data))

    def test_create_driver(self):
        data = {
            "first_name": "aaaa",
            "last_name": "aaaa",
            "number": 444,
            "country": "United Kingdom",
            "podiums": 128,
            "points": 2866,
            "championships": 4,
            # TODO figure out format for date submission
            "birthday": "Mon, 07 Jan 1985 00:00:00 -0000",
            "team_id": 1
        }
        response = self.client.post('/drivers',
                                    data=json.dumps(data),
                                    headers={'Content-Type': 'application/json',
                                             'Authorization': self.token})
        self.assertEqual(response.status_code, 201)
        expected = {
            "id": 1,
            "name": "aaaa aaaa",
            "number": 444,
            "team_id": 1,
            "country": "United Kingdom",
            "podiums": 0,
            "points": 0,
            "championships": 0,
            "birthday": "1/1/1990"
        }
        self.assertDictEqual(json.loads(response.data), expected)

    def test_driver_put(self):
        DriverModel('test fn', 'test ln', 0, 1, 'test', 0, 0, 0, date(1995, 8, 25)).save_to_db()
        headers = {'Authorization': self.token,
                   'Content-Type': 'application/json'}
        data = json.dumps({
            "first_name": "new test fn",
            "last_name": "new test ln",
            "number": 1,
            "team_id": 1,
            "country": "new test"
        })
        response = self.client.put('/drivers/1', data=data, headers=headers)
        self.assertEqual(response.status_code, 202)
        expected = {
            'id': 1,
            'first_name': 'new test fn',
            'last_name': 'new test ln',
            'number': 1,
            'team':
                {'base': None,
                 'car': None,
                 'championships': 0,
                 'chief': None,
                 'id': 0,
                 'name': None,
                 'power_unit': None,
                 'since': None},
            'country': 'new test',
            'podiums': 0,
            'points': 0,
            'championships': 0,
            'birthday': 'Fri, 25 Aug 1995 00:00:00 -0000',
        }
        self.assertDictEqual(expected, json.loads(response.data))

    def test_get_driver_list(self):
        driver1 = DriverModel('test fn', 'test ln', 0, 1, 'test', 0, 0, 0, date(1995, 8, 25))
        driver2 = DriverModel('test fn2', 'test ln2', 1, 1, 'test', 0, 0, 0, date(1995, 8, 25))
        driver1.save_to_db()
        driver2.save_to_db()
        headers = {'Authorization': self.token}
        response = self.client.get('/drivers', headers=headers)
        self.assertEqual(response.status_code, 200)
        expected = {
            'drivers':
            [
                {'id': 1,
                 'first_name': 'test fn',
                 'last_name': 'test ln',
                 'number': 0,
                 'country': 'test',
                 'podiums': 0,
                 'points': 0,
                 'championships': 0,
                 'birthday': 'Fri, 25 Aug 1995 00:00:00 -0000',
                 'team':
                     {'id': 0, 'name': None, 'base': None, 'chief': None, 'car': None, 'power_unit': None,
                      'since': None, 'championships': 0}},
                {'id': 2,
                 'first_name': 'test fn2',
                 'last_name': 'test ln2',
                 'number': 1,
                 'country': 'test',
                 'podiums': 0,
                 'points': 0,
                 'championships': 0,
                 'birthday': 'Fri, 25 Aug 1995 00:00:00 -0000',
                 'team':
                     {'id': 0, 'name': None, 'base': None, 'chief': None, 'car': None, 'power_unit': None,
                      'since': None, 'championships': 0}}
            ]
        }
        self.assertDictEqual(expected, json.loads(response.data))

    def test_get_driver_list_no_auth(self):
        driver1 = DriverModel('test fn', 'test ln', 0, 1, 'test', 0, 0, 0, date(1995, 8, 25))
        driver2 = DriverModel('test fn2', 'test ln2', 1, 1, 'test', 0, 0, 0, date(1995, 8, 25))
        driver1.save_to_db()
        driver2.save_to_db()
        response = self.client.get('/drivers')
        self.assertEqual(response.status_code, 200)
        expected = {
            'drivers':
            [
                {'first_name': 'test fn',
                 'last_name': 'test ln',
                 'number': 0
                 },
                {'first_name': 'test fn2',
                 'last_name': 'test ln2',
                 'number': 1}
            ],
            'message': 'More information if logged in.'
        }
        self.assertDictEqual(expected, json.loads(response.data))
