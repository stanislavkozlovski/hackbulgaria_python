import unittest
import sqlite3
import sys
from io import StringIO
import database_gui as db
from database_scripts import CREATE_TABLES_SCRIPT, DROP_TABLES_SCRIPT


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        db.connection = sqlite3.connect(db.DB_PATH + '_test')
        db.cursor = db.connection.cursor()
        # create the db
        db.cursor.executescript(CREATE_TABLES_SCRIPT)
        self.db = db

    def tearDown(self):
        db.cursor.executescript(DROP_TABLES_SCRIPT)
        db.connection.commit()
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

    def test_add_patient(self):
        patient_name = "Vasko"
        patient_lastname = "Vasilev"
        patient_age = 15
        patient_gender = "male"
        patient_doctor = None
        user_input = "{name}\n{lastname}\n{age}\n{gender}\n{doctor}".format(
            name=patient_name, lastname=patient_lastname, age=patient_age,
            gender=patient_gender, doctor=patient_doctor
        )
        try:
            sys.stdin = StringIO(user_input)
            self.db.add_patient()
            patient = db.cursor.execute("SELECT * FROM PATIENTS").fetchone()
            self.assertEqual(patient, (1, patient_name, patient_lastname, patient_age, patient_gender, patient_doctor))
        finally:
            sys.stdin = sys.__stdin__

if __name__ == '__main__':
    unittest.main()