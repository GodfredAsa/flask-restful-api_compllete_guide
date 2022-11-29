import json
from models.user import UserModel
from tests.system_base_test import SystemBaseTest

class UserTest(SystemBaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                response = client.post("/register", data={"username": "test", "password": "1234"})

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username("test"))

                self.assertDictEqual({"message": "User created successfully."},
                                     # converts response to dictionary
                                     json.loads(response.data))

    # TODO WRITE TESTS FOR REFRESH TOKEN ENDPOINT
    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                user_data = {'username': 'test', 'password': '1234'}
                client.post('/register', data=user_data)
                # data converted to json
                auth_response = client.post('/login',
                                            data=json.dumps(user_data),
                                            headers={'Content-Type': 'application/json'})
                # checking that the response contains access token and refresh token
                self.assertIn('access_token', json.loads(auth_response.data).keys())
                self.assertIn('refresh_token', json.loads(auth_response.data).keys())

    # double registration or register duplicate below
    def test_user_exists(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': '1234'})
                response = client.post("/register", data={"username": "test", "password": "1234"})
                self.assertEqual(response.status_code, 400, 'user already exists')
                self.assertDictEqual({'message': 'A user with that username already exists.'}, json.loads(response.data))
