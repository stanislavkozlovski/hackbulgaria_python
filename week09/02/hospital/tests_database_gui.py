import unittest
import sqlite3
import sys
from io import StringIO
import database_gui as db


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        db.connection = sqlite3.connect(db.DB_PATH)
        db.cursor = db.connection.cursor()
        self.db = db

    def tearDown(self):
        db.connection.close()

    def test_create(self):
        expected_output = """TABLES CREATED!
"""
        output = StringIO()
        try:
            sys.stdout = output
            self.db.create_tables()
            self.assertEqual(output.getvalue(), expected_output)
        finally:
            sys.stdout = sys.__stdout__


if __name__ == '__main__':
    unittest.main()