import json
from typing import Dict, Any
from models.item import ItemModel
from models.store import StoreModel
from tests.system_base_test import SystemBaseTest

class ItemTest(SystemBaseTest):
    def setUp(self) -> Dict[str, Any]:
        super(ItemTest, self).setUp()  # calls the setup method of the base class
        with self.app() as client:
            with self.app_context():
                user_data = {'username': 'test', 'password': '1234'}
                client.post('/register', data=user_data)
                # data converted to json
                auth_response = client.post('/login',
                                            data=json.dumps(user_data),
                                            headers={'Content-Type': 'application/json'})

                return {"access_token": json.loads(auth_response.data)['access_token'],
                        "refresh_token": json.loads(auth_response.data)['refresh_token']}

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                ItemModel('test', 19.9, 1).save_to_db()
                response = client.get('/item/test')
                self.assertEqual(200, response.status_code)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/test')
                self.assertEqual(404, response.status_code)

    def test_delete_item_not_authenticated(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('store').save_to_db()  # Postgres/MYSQL dont save a store, sqlite need to
                ItemModel('test', 19.9, 1).save_to_db()
                response = client.delete('/item/test')
                self.assertEqual(401, response.status_code)
                # self.assertDictEqual({'message': 'Item deleted'}, json.loads(response.data))

    def test_delete_item_authenticated(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('store').save_to_db()  # Postgres/MYSQL dont save a store, sqlite need to
                ItemModel('test', 19.9, 1).save_to_db()
                access_token = self.setUp()["access_token"]
                client.delete('/item/test', headers={'Authorization': f'Bearer {access_token}'})
                self.assertIsNone(ItemModel.find_by_name('test'), "Item deleted with access token")

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                # client.post('/store/my-store')
                StoreModel('store').save_to_db()
                # Postgres/MYSQL dont save a store, sqlite need to
                access_token = self.setUp()["access_token"]
                client.post('/item/test',
                            data={'price': 19.9, 'store_id': 1},
                            headers={'Authorization': f'Bearer {access_token}'})
                self.assertIsNotNone(ItemModel.find_by_name('test'), "Item created with refresh token")

    # TODO: TEST THE FOLLOWING FUNCTIONS
    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('store').save_to_db()
                access_token = self.setUp()["access_token"]

                # Postgres/MYSQL don't save a store, sqlite need to
                # create the item and assert is not none
                client.post('/item/test',
                            data={'price': 19.9, 'store_id': 1},
                            headers={'Authorization': f'Bearer {access_token}'})

                self.assertIsNotNone(ItemModel.find_by_name('test'), "Item created with refresh token")

                # create the item and assert is 400 and message of item already exists
                response = client.post('/item/test',
                                       data={'price': 19.9, 'store_id': 1},
                                       headers={'Authorization': f'Bearer {access_token}'})

                self.assertEqual(400, response.status_code)
                self.assertDictEqual({'message': "An item with name \'test\' already exists."},
                                     json.loads(response.data))

    # creates the item if item does not exist
    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('store').save_to_db()
                response = client.put('/item/test', data={'price': 200.99, 'store_id': 1})
                self.assertEqual(200, response.status_code)
                self.assertEqual(ItemModel.find_by_name('test').price, 200.99, 'comparing price')
                self.assertDictEqual({'id': 1, 'name': 'test', 'price': 200.99, 'store_id': 1},
                                     json.loads(response.data))

    # updates the item if it exists
    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('store').save_to_db()
                access_token = self.setUp()["access_token"]
                # creating an item
                client.post('/item/test',
                            data={'price': 19.9, 'store_id': 1},
                            headers={'Authorization': f'Bearer {access_token}'})

                self.assertIsNotNone(ItemModel.find_by_name('test'), "Item created with access token")

                # updating existing item
                response = client.put('/item/test', data={'price': 200.99, 'store_id': 1})
                self.assertEqual(200, response.status_code)
                self.assertEqual(200.99, ItemModel.find_by_name('test').price, "checks updated price")
                self.assertDictEqual({'id': 1, 'name': 'test', 'price': 200.99, 'store_id': 1},
                                     json.loads(response.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                ItemModel('test', 19.9, 1).save_to_db()  # Postgres/MYSQL dont save a store, sqlite need to
                ItemModel('test-2', 69.9, 1).save_to_db()
                response = client.get('/items')
                self.assertEqual(200, response.status_code)

                expected = {"items":
                                [{"id": 1, "name": "test", "price": 19.9, "store_id": 1},
                                 {"id": 2, "name": "test-2", "price": 69.9, "store_id": 1}]
                            }
                actual = json.loads(response.data)
                self.assertDictEqual(expected, actual)