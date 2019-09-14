from unittest import TestCase
from datetime import date
from api.app.models import DriverModel


class DriverTest(TestCase):
    def test_create_driver(self):
        driver = DriverModel('test fn', 'test ln', 0, 1, 'test', 0, 0, 0, date(1995, 8, 25))
        self.assertIsNotNone(driver)
        self.assertEqual(driver.first_name, 'test fn')
        self.assertEqual(driver.last_name, 'test ln')
        self.assertEqual(driver.number, 0)
        self.assertEqual(driver.team_id, 1)
        self.assertEqual(driver.country, 'test')
        self.assertEqual(driver.podium, 0)
        self.assertEqual(driver.points, 0)
        self.assertEqual(driver.championships, 0)
        self.assertEqual(driver.birthday, date(1995, 8, 25))

