import unittest
from Store.client import Client
from Store.order import Order
from Store.products.computer import Computer
from Store.products.tv import Tv
from Store.reporting import Reporting
from Store.store import Store
from Store.user import User
from Store.storeerror import StoreError


class TestStore(unittest.TestCase):

    def setUp(self):
        self.store = Store()
        self.store.reporting = Reporting()
        self.store.users = {}
        self.store.collection = {}
        self.store.orders = {}
        self.store.order_number = 1

    def test_add_user(self):
        user = {"user_id": "1234", "user_type": "CLIENT", "user_full_name": "John Doe", "password": "password123"}  # שינוי
        result = self.store.add_user(user)
        self.assertTrue(result)
        self.assertIn("1234", self.store.users)
        self.assertEqual(self.store.users["1234"].user_full_name, "John Doe")
        self.assertEqual(self.store.sales.get_coupon_discount("1234"), 5)

    def test_add_review(self):
        product = Tv(name="Samsung TV", price=500, quantity=10, model="QLED", description="A great TV")
        self.store.collection[product.get_key_name()] = product
        result = self.store.add_review(product.get_key_name(), 5, "Great TV!")
        self.assertTrue(result)
        self.assertEqual(len(self.store.collection[product.get_key_name()].rate.rating[5]), 1)

    def test_add_review_non_existing_product(self):
        result = self.store.add_review("non_existing", 5, "Great product!")
        self.assertFalse(result)

    def test_add_product(self):
        product_dict = {
            "name": "Laptop",
            "price": 1500,
            "quantity": 10,
            "model": "L123",
            "product_type": "Computer",
            "description": "High performance laptop"
        }
        self.store.add_product(product_dict)

    def test_add_existing_product(self):
        product_dict = {
            "name": "Laptop",
            "price": 1500,
            "quantity": 10,
            "model": "L123",
            "product_type": "Computer",
            "description": "High performance laptop"
        }
        self.store.add_product(product_dict)

    def test_remove_discount(self):
        product = Tv(name="Samsung TV", price=500, quantity=10, model="QLED", description="A great TV")
        self.store.collection[product.get_key_name()] = product
        self.store.sales.add_promotion(product.get_key_name(), 10)
        self.store.remove_promotion(product)
        self.assertEqual(self.store.collection[product.get_key_name()].price, 500)

    def test_search_product_by_name(self):
        product = Tv(name="Samsung TV", price=500, quantity=10, model="QLED", description="A great TV")
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
        with self.assertRaises(StoreError.AuthenticationError):
            self.store.log(user_id="user1", password="wrongpassword")

    def test_set_address(self):
        user = User(user_id="user1", user_full_name="John Doe", password="password123", address="Old Address")
        self.store.users[user.user_id] = user
        result = self.store.set_address(user_id="user1", address="New Address")
        self.assertTrue(result)
        self.assertEqual(self.store.users[user.user_id].address, "New Address")

    def test_remove_client(self):
        client = Client(user_id="client1", user_full_name="Client User", password="password123")
        self.store.users[client.user_id] = client
        result = self.store.remove_client(client.user_id)
        self.assertTrue(result)
        self.assertNotIn(client.user_id, self.store.users)

    def test_new_discount_on_specific_product(self):
        product = Tv(name="Samsung TV", price=500, quantity=10, model="QLED", description="A great TV")
        self.store.collection[product.get_key_name()] = product
        self.store.new_promotion(product, 10)
        self.assertEqual(self.store.collection[product.get_key_name()].price, 450)

    def test_new_discount_on_product_list(self):
        product1 = Tv(name="Samsung TV1", price=500, quantity=10, model="QLED1", description="A great TV")
        product2 = Tv(name="Samsung TV2", price=1000, quantity=5, model="QLED2", description="A great TV")
        self.store.collection[product1.get_key_name()] = product1
        self.store.collection[product2.get_key_name()] = product2
        self.store.new_promotion(product1, 20)
        self.store.new_promotion(product2, 20)
        self.assertEqual(self.store.collection[product1.get_key_name()].price, 400)
        self.assertEqual(self.store.collection[product2.get_key_name()].price, 800)

    def test_use_coupon(self):
        client = Client(user_id="client1", user_full_name="Client User", password="password123")
        self.store.users[client.user_id] = client
        self.store.sales.add_coupon(client.user_id, 5)
        self.store.sales.use_coupon_discount(client.user_id)
        self.assertEqual(self.store.sales.get_coupon_discount(client.user_id), 0)

    def test_sale_product_type(self):
        category = self.store.sale_prodduct_type("1", 10)
        self.assertIn(category, self.store.sales.category_discounts)
        self.assertEqual(self.store.sales.category_discounts[category], 10)

    def test_lst_search(self):
        product1 = Tv(name="Samsung TV1", price=500, quantity=10, model="QLED1", description="A great TV")
        product2 = Computer(name="Laptop", price=1500, quantity=5, model="L123", description="High performance laptop")
        self.store.collection[product1.get_key_name()] = product1
        self.store.collection[product2.get_key_name()] = product2
        item_dict = {product1.get_key_name(): 1, product2.get_key_name(): 1}
        result = self.store.lst_search(item_dict)
        self.assertEqual(result, [product1, product2])

    def test_change_order(self):
        client = Client(user_id="user1", user_full_name="John Doe", password="password123")
        self.store.users[client.user_id] = client
        product = Tv(name="Samsung TV", price=500, quantity=10, model="QLED", description="A great TV")
        self.store.collection[product.get_key_name()] = product
        order = Order(order_number=1, customer=client, product_dict={product.get_key_name(): 2},
                      payment={"owner": "John Doe", "info": "1234567812345678", "payment_method": "Credit Card",
                               "amount_of_payments": 1}, total_amount=1000, currency="₪ILS")
        self.store.orders[1] = order
        self.store.change_order(1, 1)
        self.assertEqual(self.store.orders[1].status, 'Shipped')
        self.assertEqual(self.store.users[client.user_id].order_history[1].status, 'Shipped')

    def test_list_products(self):
        product1 = Tv(name="Samsung TV1", price=500, quantity=10, model="QLED1", description="A great TV")
        product2 = Computer(name="Laptop", price=1500, quantity=5, model="L123",
                            description="High performance laptop")
        self.store.collection[product1.get_key_name()] = product1
        self.store.collection[product2.get_key_name()] = product2
        result = self.store.list_products()
        self.assertIn("SamsungTV1", result)
        self.assertIn("Laptop", result)

    def test_list_orders(self):
        user = User(user_id="user1", user_full_name="John Doe", password="password123")
        self.store.users[user.user_id] = user
        order = Order(order_number=1, customer=user, product_dict={"TV1": 1}, payment={"owner": "John Doe", "info": "1234567812345678", "payment_method": "Credit Card", "amount_of_payments": 1}, total_amount=500, currency="₪ILS", status="Pending")
        self.store.orders[1] = order
        result = self.store.list_orders()
        self.assertIn("Order number:1", result)
        self.assertIn("Pending", result)

if __name__ == '__main__':
    unittest.main()
