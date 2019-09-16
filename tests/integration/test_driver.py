from datetime import date
from tests.base_test import BaseTest
from api.app.models import DriverModel, TeamModel


class DriverTest(BaseTest):
    def test_driver_crud(self):
        TeamModel('test', 'test', 'test', 'test', 'test', 0, 0).save_to_db()
        driver = DriverModel('test fn', 'test ln', 0, 1, 'test', 0, 0, 0, date(1995, 8, 25))

        self.assertIsNone(DriverModel.find_by_id(1),
                          "Found an driver with id: 1, but expected not to.")

        driver.save_to_db()
        self.assertIsNotNone(DriverModel.find_by_id(1),
                             "Did not find an item with id: 1, but expected to.")

        driver.delete_from_db()
        self.assertIsNone(DriverModel.find_by_id(1),
                          "Found an driver with id: 1, but expected not to.")
    
    def test_team_relationship(self):
        TeamModel('test team', 'test', 'test', 'test', 'test', 0, 0).save_to_db()
        DriverModel('test fn', 'test ln', 0, 1, 'test', 0, 0, 0, date(1995, 8, 25)).save_to_db()
        driver = DriverModel.find_by_id(1)
        self.assertEqual('test tteam', driver.team.name)

    def test_driver_json(self):
        driver = DriverModel('test fn', 'test ln', 0, 1, 'test', 0, 0, 0, date(1995, 8, 25))
        driver.save_to_db()
        expected = {
            'id': 1,
            'name': "test fn test ln",
            'number': 0,
            'team_id': 1,
            'country': 'test',
            'podiums': 0,
            'points': 0,
            'championships': 1,
            'birthday': '8/25/1995',
        }
        self.assertDictEqual(driver.json(), expected)

