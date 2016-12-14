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
            sys.stdout = StringIO()
            self.db.add_patient()
            patient = db.cursor.execute("SELECT * FROM PATIENTS").fetchone()
            self.assertEqual(patient, (1, patient_name, patient_lastname, patient_age, patient_gender, patient_doctor))
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__

    def test_add_doctor(self):
        doctor_name = "Doctor"
        doctor_lastname = "McDoctorFace"
        user_input = "{name}\n{lastname}".format(
            name=doctor_name,
            lastname=doctor_lastname
        )
        try:
            sys.stdin = StringIO(user_input)
            sys.stdout = StringIO()
            self.db.add_doctor()
            doctor = db.cursor.execute("SELECT * FROM DOCTORS").fetchone()
            self.assertEqual(doctor, (1, doctor_name, doctor_lastname))
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__

    def test_add_hospital_stay(self):
        self.test_add_patient()  # to add the patient Vasko
        patient_name = "Vasko"
        user_input = "{patient_name}\n{room}\n{startdate}\n{enddate}\n{injury}".format(
            patient_name=patient_name, room=205, startdate="10-12-2016", enddate="12-12-2016",
            injury="Too much programming. :O"
        )
        try:
            sys.stdin = StringIO(user_input)
            sys.stdout = StringIO()
            self.db.add_hospital_stay()
            hospital_stay = db.cursor.execute("SELECT * FROM HOSPITAL_STAY").fetchone()
            self.assertEqual(hospital_stay, (1, 205, "10-12-2016", "12-12-2016", "Too much programming. :O", 1))
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__

if __name__ == '__main__':
    unittest.main()