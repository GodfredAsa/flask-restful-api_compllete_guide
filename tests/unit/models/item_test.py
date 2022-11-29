from models.item import ItemModel
from tests.unit.unit_base_test import UnitBaseTest

class ItemTest(UnitBaseTest):

    def test_create_item(self):
        item = ItemModel("test", 19.99, 1 )
        self.assertEqual(item.name, 'test', 'item name != constructed item name')
        self.assertEqual(item.price, 19.99, 'item price != constructed item price')

    def test_item_json(self):
        item = ItemModel("test", 19.99, 1)
        expected = {"id": None,"name": "test", "price": 19.99, "store_id": 1}
        actual = item.json()
        self.assertDictEqual(expected, actual,'JSON exported by the item is not the expected '
                                               'Received: {} Expected {}'.format(actual, expected))