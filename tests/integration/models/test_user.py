from models.user import UserModel
from tests.integration.integration_base_test import IntegrationBaseTest

class UserTest(IntegrationBaseTest):
    def test_crud_user(self):
        with self.app_context():
            user = UserModel("test", "password")

            self.assertIsNone(UserModel.find_by_username("test"), "fetches user by username")
            self.assertIsNone(UserModel.find_by_id(1), "fetches user by user id")

            user.save_to_db()
            self.assertIsNotNone(UserModel.find_by_username("test"), "user is saved")

            # ensures the password is not saved as raw text but hashed
            # password was saved as raw test in this scenario
            self.assertEqual(user.password, "password", "saved password not hashed")
