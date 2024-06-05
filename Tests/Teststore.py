import unittest
from Store.store import Store
from Store.user import User
from Store.client import Client
from Store.reporting import Reporting
from Store.product import Product
from Store.tv import Tv
from Store.computer import Computer
from Store.phone import Phone
from Store.order import Order

class TestStore(unittest.TestCase):

    def setUp(self):
        self.store = Store()
        self.store.reporting = Reporting()
        self.store.users = {}
        self.store.collection = {}
        self.store.orders = {}
        self.store.order_number = 1

    def test_add_user(self):
        user = {"user_id": "user1", "user_type": "CLIENT", "user_full_name": "John Doe"}
        result = self.store.add_user(user)
        self.assertTrue(result)
        self.assertIn("user1", self.store.users)
        self.assertEqual(self.store.users["user1"].user_full_name, "John Doe")
        self.assertEqual(self.store.users["user1"].coupon, 5)

    def test_add_existing_user(self):
        user = {"user_id": "user1", "user_type": "CLIENT", "user_full_name": "John Doe"}
        self.store.add_user(user)
        result = self.store.add_user(user)
        self.assertFalse(result)

    def test_add_review(self):
        product = Tv(name="Samsung TV", price=500, quantity=10, model="QLED")
        self.store.collection[product.get_key_name()] = product
        result = self.store.add_review(product.get_key_name(), 5, "Great TV!")
        self.assertTrue(result)
        self.assertEqual(len(self.store.collection[product.get_key_name()].reviews), 1)

    def test_add_review_non_existing_product(self):
        result = self.store.add_review("non_existing", 5, "Great product!")
        self.assertFalse(result)

    def test_add_product(self):
        product_dict = {"name": "Laptop", "price": 1500, "quantity": 10, "model": "L123", "product_type": "Computer"}
        result = self.store.add_product(product_dict)
        self.assertTrue(result)
        self.assertIn("LaptopL123", self.store.collection)

    def test_add_existing_product(self):
        product_dict = {"name": "Laptop", "price": 1500, "quantity": 10, "model": "L123", "product_type": "Computer"}
        self.store.add_product(product_dict)
        result = self.store.add_product(product_dict)
        self.assertFalse(result)

    def test_remove_discount(self):
        product = Tv(name="Samsung TV", price=500, quantity=10, model="QLED")
        self.store.collection[product.get_key_name()] = product
        result = self.store.remove_discount(product)
        self.assertTrue(result)

    def test_remove_discount_all(self):
        product = Tv(name="Samsung TV", price=500, quantity=10, model="QLED")
        self.store.collection[product.get_key_name()] = product
        result = self.store.remove_discount()
        self.assertTrue(result)

    def test_place_order(self):
        user = User(user_id="user1", user_full_name="John Doe")
        self.store.users[user.user_id] = user
        product = Tv(name="Samsung TV", price=500, quantity=10, model="QLED")
        self.store.collection[product.get_key_name()] = product
        order = Order(customer=user, product_dict={product.get_key_name(): 2}, payment="Credit Card")
        self.store.place_order(order)
        self.assertIn(self.store.order_number - 1, self.store.orders)
        self.assertEqual(self.store.orders[self.store.order_number - 1].total_amount, 1000)
        self.assertEqual(self.store.collection[product.get_key_name()].quantity, 8)

    def test_search_product_by_name(self):
        product = Tv(name="Samsung TV", price=500, quantity=10, model="QLED")
        self.store.collection[product.get_key_name()] = product
        result = self.store.search(name="Samsung")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Samsung TV")

    def test_log_valid_user(self):
        user = User(user_id="user1", user_full_name="John Doe", password="password123")
        self.store.users[user.user_id] = user
        logged_user = self.store.log(user_id="user1", password="password123")
        self.assertEqual(logged_user, user)

    def test_log_invalid_user(self):
        user = User(user_id="user1", user_full_name="John Doe", password="password123")
        self.store.users[user.user_id] = user
        logged_user = self.store.log(user_id="user1", password="wrongpassword")
        self.assertIsNone(logged_user)

    def test_set_address(self):
        user = User(user_id="user1", user_full_name="John Doe", address="Old Address")
        self.store.users[user.user_id] = user
        result = self.store.set_address(user_id="user1", address="New Address")
        self.assertTrue(result)
        self.assertEqual(self.store.users[user.user_id].address, "New Address")

    def test_remove_client(self):
        client = Client(user_id="client1", user_full_name="Client User", coupon=5)
        self.store.users[client.user_id] = client
        result = self.store.remove_client(client.user_id)
        self.assertTrue(result)
        self.assertNotIn(client.user_id, self.store.users)

    def test_user_order_history(self):
        user = User(user_id="user1", user_full_name="John Doe")
        self.store.users[user.user_id] = user
        product = Tv(name="Samsung TV", price=500, quantity=10, model="QLED")
        self.store.collection[product.get_key_name()] = product
        order = Order(customer=user, product_dict={product.get_key_name(): 2}, payment="Credit Card")
        self.store.orders[self.store.order_number] = order
        self.store.order_number += 1
        history = self.store.user_order_history(user)
        self.assertEqual(len(history), 1)
        self.assertIn(order.order_number, history)

    def test_new_discount_on_specific_product(self):
        product = Tv(name="Samsung TV", price=500, quantity=10, model="QLED")
        self.store.collection[product.get_key_name()] = product
        self.store.new_discount(product, 10)
        self.assertEqual(self.store.collection[product.get_key_name()].price, 450)  # assuming initial price was 500 and discount is 10%

    def test_new_discount_on_product_list(self):
        product1 = Tv(name="Samsung TV1", price=500, quantity=10, model="QLED1")
        product2 = Tv(name="Samsung TV2", price=1000, quantity=5, model="QLED2")
        self.store.collection[product1.get_key_name()] = product1
        self.store.collection[product2.get_key_name()] = product2
        self.store.new_discount([product1, product2], 20)
        self.assertEqual(self.store.collection[product1.get_key_name()].price, 400)  # assuming initial price was 500 and discount is 20%
        self.assertEqual(self.store.collection[product2.get_key_name()].price, 800)  # assuming initial price was 1000 and discount is 20%

    def test_use_coupon(self):
        client = Client(user_id="client1", user_full_name="Client User", coupon=5)
        self.store.users[client.user_id] = client
        self.store.use_coupon(client)
        self.assertEqual(client.coupon, 4)

    def test_sale_product_type(self):
        self.store.sale_prodduct_type("1", 10)
        self.assertIn("* -10% discount on all TVs *", self.store.sales)

    def test_lst_search(self):
        product1 = Tv(name="Samsung TV1", price=500, quantity=10, model="QLED1")
        product2 = Computer(name="Laptop", price=1500, quantity=5, model="L123")
        self.store.collection[product1.get_key_name()] = product1
        self.store.collection[product2.get_key_name()] = product2
        order = Order(customer=None, product_dict={product1.get_key_name(): 1, product2.get_key_name(): 1})
        result = self.store.lst_search(order)
        self.assertEqual(result, [product1, product2])

    def test_change_order(self):
        user = User(user_id="user1", user_full_name="John Doe")
        self.store.users[user.user_id] = user
        product = Tv(name="Samsung TV", price=500, quantity=10, model="QLED")
        self.store.collection[product.get_key_name()] = product
        order = Order(customer=user, product_dict={product.get_key_name(): 2}, payment="Credit Card")
        self.store.orders[1] = order
        self.store.change_order(1, "Shipped")
        self.assertEqual(self.store.orders[1].status, "Shipped")
        self.assertEqual(self.store.users[user.user_id].order_history[1].status, "Shipped")

    def test_load_files(self):
        # Assuming DataManager mock or actual methods to load data
        self.store.load_files()
        self.assertGreater(len(self.store.users), 0)
        self.assertGreater(len(self.store.collection), 0)
        self.assertGreater(len(self.store.orders), 0)
        self.assertGreater(len(self.store.sales), 0)

    def test_save_files(self):
        # Assuming DataManager mock or actual methods to save data
        self.store.users["user1"] = User(user_id="user1", user_full_name="John Doe")
        self.store.collection["TV1"] = Tv(name="Samsung TV1", price=500, quantity=10, model="QLED1")
        self.store.orders[1] = Order(customer=self.store.users["user1"], product_dict={"TV1": 1}, payment="Credit Card")
        self.store.save_files()
        # No assertion, just ensure no exceptions

    def test_list_products(self):
        product1 = Tv(name="Samsung TV1", price=500, quantity=10, model="QLED1")
        product2 = Computer(name="Laptop", price=1500, quantity=5, model="L123")
        self.store.collection[שׂproduct1.get_key_name()] = product1
        self.store.collection[product2.get_key_name()] = product2
        result = self.store.list_products()
        self.assertIn(("Samsung TV1", "QLED1", "Price: 500 ₪ ", "Available: 10"), result)
        self.assertIn(("Laptop", "L123", "Price: 1500 ₪ ", "Available: 5"), result)

    def test_list_orders(self):
        user = User(user_id="user1", user_full_name="John Doe")
        self.store.users[user.user_id] = user
        order = Order(customer=user, product_dict={"TV1": 1}, total_amount=500, status="Pending")
        self.store.orders[1] = order
        result = self.store.list_orders()
        self.assertIn([1, "John Doe", 500, "Pending"], result)

if __name__ == '__main__':
    unittest.main()
