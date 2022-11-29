from models.store import StoreModel
from tests.unit.unit_base_test import UnitBaseTest

class StoreTest(UnitBaseTest):

    def test_create_store(self):
        store = StoreModel("test" )
        self.assertEqual(store.name, 'test', 'item name != constructed item name')

    def test_store_json(self):
        store = StoreModel("test" )
        expected = {"id": None, "name": "test", "items":[]}
        actual = store.json()
        self.assertDictEqual(expected, actual,'JSON exported by the item is not the expected '
                                               'Received: {} Expected {}'.format(actual, expected))