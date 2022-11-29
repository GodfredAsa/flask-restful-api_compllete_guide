from models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest

class UserTest(UnitBaseTest):

    def test_create_user(self):
       user = UserModel("test", "1234")
       self.assertEqual(user.username, 'test')
       self.assertEqual(user.password, "1234")

    def test_user_json(self):
        user = UserModel("test", "1234")
        expected = {"id": None,"username": "test"}
        actual = user.json()
        self.assertDictEqual(expected, actual,'JSON exported by the item is not the expected '
                                               'Received: {} Expected {}'.format(actual, expected))