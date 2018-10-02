from api.app.models import DriverModel, TeamModel, UserModel
from tests.base_test import BaseTest
import json
from datetime import date


class TeamTest(BaseTest):
    def setUp(self):
        super(TeamTest, self).setUp()
        UserModel('test', 'password', True).save_to_db()
        auth_response = self.client.post('/login',
                                         data=json.dumps({'username': 'test', 'password': 'password'}),
                                         headers={'Content-Type': 'application/json'})
        self.token = 'Bearer {}'.format(json.loads(auth_response.data).get('access_token'))

    def test_create_team(self):
        headers = {'Authorization': self.token,
                   'Content-Type': 'application/json'}
        data = {
            'name': 'test',
            'base': 'test',
            'chief': 'test',
            'car': 'test',
            'power_unit': 'test'
        }

        response = self.client.post('/teams/1',
                                    data=json.dumps(data),
                                    headers=headers)
        self.assertEqual(response.status_code, 201)

        expected = {
            "id": 1,
            "name": "test",
            "base": "test",
            "chief": "test",
            "car": "test",
            "power_unit": "test",
            "founded": 0,
            "championships": 0,
            "drivers": []
        }
        self.assertDictEqual(expected, json.loads(response.data))

    def test_create_duplicate_team(self):
        TeamModel('test team', 'test', 'test', 'test', 'test', 0, 0).save_to_db()
        headers = {'Authorization': self.token,
                   'Content-Type': 'application/json'}
        data = {
            'name': 'test',
            'base': 'test',
            'chief': 'test',
            'car': 'test',
            'power_unit': 'test'
        }

        response = self.client.post('/teams/1',
                                    data=json.dumps(data),
                                    headers=headers)
        self.assertEqual(response.status_code, 400)
        expected = {"message": "Team with id:1 already exists"}
        self.assertDictEqual(expected, json.loads(response.data))

    def test_delete_team(self):
        TeamModel('test team', 'test', 'test', 'test', 'test', 0, 0).save_to_db()
        headers = {'Authorization': self.token}
        response = self.client.delete('/teams/1',
                                      headers=headers)
        self.assertEqual(response.status_code, 202)
        self.assertDictEqual({'message': 'Team id:1 deleted.'}, json.loads(response.data))

    def test_get_team(self):
        TeamModel('test team', 'test', 'test', 'test', 'test', 0, 0).save_to_db()
        response = self.client.get('/teams/1')
        self.assertEqual(response.status_code, 200)
        expected = {
            'id': 1,
            'name': 'test team',
            'base': 'test',
            'chief': 'test',
            'car': 'test',
            'power_unit': 'test',
            'since': '0',
            'championships': 0,
            'drivers': []
        }
        self.assertDictEqual(expected, json.loads(response.data))

    def test_team_not_fount(self):
        response = self.client.get('/teams/1')

        self.assertEqual(response.status_code, 404)
        self.assertDictEqual(json.loads(response.data),
                             {'message': "TeamId:1 not found"})

    def test_team_found_with_drivers(self):
        TeamModel('test team', 'test', 'test', 'test', 'test', 0, 0).save_to_db()
        DriverModel('test fn', 'test ln', 0, 1, 'test', 0, 0, 0, date(1995, 8, 25)).save_to_db()
        response = self.client.get('/teams/1')
        self.assertEqual(200, response.status_code)
        expected = {
            'id': 1,
            'name': 'test team',
            'base': 'test',
            'chief': 'test',
            'car': 'test',
            'power_unit': 'test',
            'since': '0',
            'championships': 0,
            'drivers':
                [
                    {'id': 1, 'first_name': 'test fn', 'last_name': 'test ln', 'number': 0, 'points': 0}
                ]
        }
        self.assertDictEqual(expected, json.loads(response.data))

    def test_team_list(self):
        TeamModel('test team', 'test', 'test', 'test', 'test', 0, 0).save_to_db()
        TeamModel('test team2', 'test2', 'test2', 'test2', 'test2', 0, 0).save_to_db()
        response = self.client.get('/teams')
        self.assertEqual(200, response.status_code)
        expected = {
            'teams':
                [
                    {
                        'id': 1,
                        'name': 'test team',
                        'base': 'test',
                        'chief': 'test',
                        'car': 'test',
                        'power_unit': 'test',
                        'since': '0',
                        'championships': 0,
                        'drivers': []
                    },
                    {
                        'id': 2,
                        'name': 'test team2',
                        'base': 'test2',
                        'chief': 'test2',
                        'car': 'test2',
                        'power_unit': 'test2',
                        'since': '0',
                        'championships': 0,
                        'drivers': []
                    }
                ]
        }
        self.assertDictEqual(expected, json.loads(response.data))

    def test_team_list_with_drivers(self):
        TeamModel('test team', 'test', 'test', 'test', 'test', 0, 0).save_to_db()
        DriverModel('test fn', 'test ln', 0, 1, 'test', 0, 0, 0, date(1995, 8, 25)).save_to_db()

        response = self.client.get('/teams')
        self.assertEqual(200, response.status_code)
        expected = {
            'teams':
                [
                    {
                        'id': 1,
                        'name': 'test team',
                        'base': 'test',
                        'chief': 'test',
                        'car': 'test',
                        'power_unit': 'test',
                        'since': '0',
                        'championships': 0,
                        'drivers':
                            [
                                {'id': 1, 'first_name': 'test fn', 'last_name': 'test ln', 'number': 0, 'points': 0}
                            ]
                    }
                ]
        }
        self.assertDictEqual(expected, json.loads(response.data))


