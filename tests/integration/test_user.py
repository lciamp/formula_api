from tests.base_test import BaseTest
from api.app.models import UserModel


class TestUser(BaseTest):
    def test_user_crud(self):
        user = UserModel('Test', 'password', False)

        self.assertIsNone(user.find_by_username('Test'),
                          "Found a user with name '{}', but expected not to.".format(user.username))
        self.assertIsNone(user.find_by_id(1),
                          "Found a user with id: 1, but expected not to.")

        user.save_to_db()

        self.assertIsNotNone(user.find_by_username('Test'),
                             "Did not find a user with name '{}', but expected to.".format(user.username))
        self.assertIsNotNone(user.find_by_id(1),
                             "Did not find a user with id: 1, but expected to.")

        user.delete_from_db()

        self.assertIsNone(user.find_by_username('Test'),
                          "Found a user with name '{}', but expected not to.".format(user.username))
        self.assertIsNone(user.find_by_id(1),
                          "Found a user with id: 1, but expected not to.")