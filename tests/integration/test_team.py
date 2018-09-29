from tests.base_test import BaseTest
from api.app.models import DriverModel, TeamModel
from datetime import date


class TeamTest(BaseTest):
    def test_create_team_drivers_empty(self):
        TeamModel('test team', 'test', 'test', 'test', 'test', 0, 0).save_to_db()

        team = TeamModel.find_by_name('test team')

        self.assertListEqual(team.drivers.all(), [])

    def test_team_crud(self):
        team = TeamModel('test team', 'test', 'test', 'test', 'test', 0, 0)

        self.assertIsNone(team.find_by_name('test team'),
                          "Found a team with name '{}', but expected not to.".format(team.name))

        team.save_to_db()

        self.assertIsNotNone(team.find_by_name('test team'),
                             "Did not find a team with name '{}', but expected to.".format(team.name))

        team.delete_from_db()

        self.assertIsNone(team.find_by_name('test team'),
                          "Found a team with name '{}', but expected not to.".format(team.name))

    def test_driver_relationship(self):
        TeamModel('test team', 'test', 'test', 'test', 'test', 0, 0).save_to_db()
        DriverModel('test fn', 'test ln', 0, 1, 'test', 0, 0, 0, date(1995, 8, 25)).save_to_db()
        team = TeamModel.find_by_name('test team')

        self.assertEqual(team.drivers.count(), 1)
        self.assertEqual(team.drivers.first().first_name, 'test fn')

    def test_team_json_with_driver(self):
        team = TeamModel('test team', 'test', 'test', 'test', 'test', 0, 0)
        driver = DriverModel('test fn', 'test ln', 0, 1, 'test', 0, 0, 0, date(1995, 8, 25))

        team.save_to_db()
        driver.save_to_db()

        expected = {
            'id': 1,
            'name': 'test team',
            'base': 'test',
            'chief': 'test',
            'car': 'test',
            'power_unit': 'test',
            'founded': 0,
            'championships': 0,
            'drivers': [driver.json()],
        }
        self.assertEqual(team.json(), expected)
