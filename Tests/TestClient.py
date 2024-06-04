import unittest
from Store.client import Client
from Store.order import Order
from Store.payment import Payment


class TestClient(unittest.TestCase):

    def setUp(self):
        self.payment = Payment("Client Check", "1234567890", "Credit Card", 10)
        self.client = Client("2020", "Client Check", '1234', 'Address', 0, "Credit Card", 10)
        self.order1 = Order(self.client, 100, {"Product1": 1}, self.payment)
        self.order2 = Order(self.client, 200, {"Product2": 2}, self.payment)

    def test_update_client(self):
        self.client.messege = ["Message 1", "Message 2"]
        self.client.new_messege = 2
        notifications = self.client.update_client()
        self.assertIn("Message 1", notifications)
        self.assertIn("Message 2", notifications)
        self.assertIn("There are 2 new notifications for you", notifications)
        self.assertEqual(self.client.new_messege, 0)
        self.assertEqual(self.client.messege, [])
        notifications = self.client.update_client()
        self.assertIn("There are no new notifications", notifications)

    def test_use_coupon(self):
        self.client.use_coupon()
        self.assertEqual(self.client.coupon, 0)

    def test_new_status(self):
        self.client.new_status(self.order1)
        self.assertIn(self.order1.order_number, self.client.order_history)
        self.assertIn(f"\n *Order Number:{self.order1.order_number} has been {self.order1.status} *", self.client.messege)
        self.assertEqual(self.client.new_messege, 1)

    def test_new_order(self):
        self.client.new_order(self.order2)
        self.assertIn(self.order2.order_number, self.client.order_history)
        self.assertIn(f"\n * Thank you for your purchase!,  Order number: {self.order2.order_number} has been received! *", self.client.messege)
        self.assertEqual(self.client.new_messege, 1)

    def test_list_orders_client(self):
        self.client.new_order(self.order1)
        self.client.new_order(self.order2)
        orders_list = self.client.list_orders_client()
        self.assertEqual(len(orders_list), 2)
        self.assertIn(f"Order Number: {self.order1.order_number}", orders_list[0][0])
        self.assertIn(f"Order Number: {self.order2.order_number}", orders_list[1][0])

    def test_change_address(self):
        new_address = "New Address"
        self.client.change_address(new_address)
        self.assertEqual(self.client.address, new_address)

    def test_str_method(self):
        client_str = str(self.client)
        self.assertIn("Client Check", client_str)
        self.assertIn("2020", client_str)


if __name__ == '__main__':
    unittest.main()
