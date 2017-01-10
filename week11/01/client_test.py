import sys
import unittest
sys.path.append("..")

from client import Client


class ClientTests(unittest.TestCase):

    def setUp(self):
        self.client_message = "Bitcoin mining makes me rich"
        self.client_balance = 200000.00
        self.client_id = 1
        self.client_username = "Ivo"
        self.client_email = 'ivo@panda.bg'
        self.test_client = Client(self.client_id, self.client_username, self.client_email, self.client_balance, self.client_message)

    def test_client_id(self):
        self.assertEqual(self.test_client.id, self.client_id)

    def test_client_name(self):
        self.assertEqual(self.test_client.username, self.client_username)

    def test_client_balance(self):
        self.assertEqual(self.test_client.balance, self.client_balance)

    def test_client_message(self):
        self.assertEqual(self.test_client.message, self.client_message)

    def test_client_set_message(self):
        self.assertEqual(self.test_client.message, self.client_message)
        self.client_message = 'AaA'
        self.test_client.message = self.client_message
        self.assertEqual(self.test_client.message, self.client_message)

    def test_client_deposit_money(self):
        self.assertEqual(self.test_client.balance, self.client_balance)
        self.test_client.deposit_money(1.1)
        self.assertEqual(self.test_client.balance, self.client_balance + 1.1)


if __name__ == '__main__':
    unittest.main()
