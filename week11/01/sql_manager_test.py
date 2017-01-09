import sys
import unittest
import os
sys.path.append("..")
if os._exists('bank.db'):
    os.remove("bank.db")

import sql_manager


class SqlManagerTests(unittest.TestCase):

    def setUp(self):
        self.tester_password = '123AaaA$RffFD'
        sql_manager.create_clients_table()
        sql_manager.register('Tester', self.tester_password)

    def tearDown(self):
        sql_manager.cursor.execute('DROP TABLE clients')

    @classmethod
    def tearDownClass(cls):
        os.remove("bank.db")

    def test_register(self):
        sql_manager.register('Dinko', '12Aa$A4Aa3123')

        sql_manager.cursor.execute('SELECT Count(*)  FROM clients WHERE username = ?', ['Dinko'])
        users_count = sql_manager.cursor.fetchone()

        self.assertEqual(users_count[0], 1)
        # assert that the invalid login table is populated with the user
        sql_manager.cursor.execute('SELECT Count(*) FROM invalid_logins WHERE id = ?', [sql_manager.get_user_id('Dinko')])

        invalid_logins_count = sql_manager.cursor.fetchone()
        self.assertEqual(invalid_logins_count[0], 1)

    def test_password_hash_on_register(self):
        dinko_pass = '12Aa$A4Aa3123'
        sql_manager.register('Dinko', dinko_pass)

        sql_manager.cursor.execute('SELECT Count(*)  FROM clients WHERE username = ?',
                                   ['Dinko'])
        users_count = sql_manager.cursor.fetchone()
        self.assertEqual(users_count[0], 1)

        user_password = sql_manager.cursor.execute('SELECT password FROM clients WHERE clients.username = "Dinko";')
        self.assertNotEqual(user_password, dinko_pass)

    def test_login(self):
        logged_user = sql_manager.login('Tester', self.tester_password)
        self.assertEqual(logged_user.username, 'Tester')

    def test_login_wrong_password(self):
        logged_user = sql_manager.login('Tester', '12Aa$3EedX3')
        self.assertFalse(logged_user)
        # assert that the invalid login table has been updated
        sql_manager.cursor.execute('SELECT login_count FROM invalid_logins WHERE id = ?',
                                   [sql_manager.get_user_id('Tester')])

        invalid_logins = sql_manager.cursor.fetchone()[0]
        self.assertEqual(invalid_logins, 1)

    def test_login_wrong_password_login_right_password_valid_invalid_logins(self):
        """
        Logging with the wrong password should set the invalid logins to 1, but logging in with the correct one
        afterwards should reset it to 0
        """
        logged_user = sql_manager.login('Tester', '12Aa$3EedX3')
        self.assertFalse(logged_user)
        # assert that the invalid login table has been updated
        sql_manager.cursor.execute('SELECT login_count FROM invalid_logins WHERE id = ?',
                                   [sql_manager.get_user_id('Tester')])

        invalid_logins = sql_manager.cursor.fetchone()[0]
        self.assertEqual(invalid_logins, 1)
        logged_user = sql_manager.login('Tester', self.tester_password)
        self.assertEqual(logged_user.username, 'Tester')
        sql_manager.cursor.execute('SELECT login_count FROM invalid_logins WHERE id = ?',
                                   [sql_manager.get_user_id('Tester')])

        invalid_logins = sql_manager.cursor.fetchone()[0]
        self.assertEqual(invalid_logins, 1)

    def test_login_sql_injection(self):
        logged_user = sql_manager.login('Tester', "' OR 1 = 1 --")
        self.assertFalse(logged_user)

    def test_change_message(self):
        logged_user = sql_manager.login('Tester', self.tester_password)
        new_message = "podaivinototam"
        sql_manager.change_message(new_message, logged_user)
        self.assertEqual(logged_user.message, new_message)

    def test_change_password(self):
        logged_user = sql_manager.login('Tester', self.tester_password)
        new_password = '12Aa$EedX3'
        sql_manager.change_pass(new_password, logged_user)

        logged_user_new_password = sql_manager.login('Tester', new_password)
        # test that it's hashed
        self.assertEqual(logged_user_new_password.username, 'Tester')

if __name__ == '__main__':
    unittest.main()
