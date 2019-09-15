from unittest import TestCase
from api.app.models import DriverModel, TeamModel


class TeamTest(TestCase):
    def test_create_team(self):
        team = TeamModel('test', 'test', 'test', 'test', 'test', 0, 0)
        self.assertIsNotNone(team)
        self.assertEqual(team.name, 'test')
        self.assertEqual(team.base, 'test')
        self.assertEqual(team.chief, 'test')
        self.assertEqual(team.car, 'test')
        self.assertEqual(team.power_unit, 'test')
        self.assertEqual(team.since, 0)
        self.assertEqual(team.championships, 0)
