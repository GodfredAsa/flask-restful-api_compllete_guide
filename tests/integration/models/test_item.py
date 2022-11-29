from models.item import ItemModel
from models.store import StoreModel
from tests.integration.integration_base_test import IntegrationBaseTest

class ItemTest(IntegrationBaseTest):
    def test_crud(self):
        with self.app_context():
            # 1 = store_id in sqlite constraints are not enforced.
            StoreModel("test")  # done for other DBMS like postgres/mysql to maintain constraints
            item = ItemModel('test', 19.99, 1)

            self.assertIsNone(ItemModel.find_by_name('test'),
                              "Found an item with name {}, but expected not to.".format(item.name))

            item.save_to_db()

            self.assertIsNotNone(ItemModel.find_by_name('test'))

            item.delete_from_db()

            self.assertIsNone(ItemModel.find_by_name('test'))

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel("test_store")
            item = ItemModel("test", 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(item.store.name, "test_store")
