import unittest
import sqlite3
import sys
from io import StringIO
import database_gui as db
from database_scripts import CREATE_TABLES_SCRIPT, DROP_TABLES_SCRIPT


class DatabaseAddTests(unittest.TestCase):
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

    def test_add_hospital_stay_invalid_patient(self):
        """ Add a hospital stay to a patient that does not exist.
            Nothing should happen """
        user_input = "{patient_name}\n".format(patient_name="NOBODY")
        output = StringIO()
        try:
            sys.stdin = StringIO(user_input)
            sys.stdout = output
            self.db.add_hospital_stay()
            # assert error message
            self.assertTrue("Such a patient does not exist!" in output.getvalue())

            potential_hospital_stay = db.cursor.execute("SELECT * FROM HOSPITAL_STAY").fetchone()
            # assert that no hospital stay was saved to the db
            self.assertEqual(potential_hospital_stay, None)
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__


class DatabaseModifyTests(unittest.TestCase):
    """ Tests that modify the database - update/delete """
    def setUp(self):
        db.connection = sqlite3.connect(db.DB_PATH + '_test')
        db.connection.row_factory = sqlite3.Row
        db.cursor = db.connection.cursor()
        # create the db
        db.cursor.executescript(CREATE_TABLES_SCRIPT)
        self.db = db
        # Create all the entities
        self.create_doctor()
        self.create_patient()
        self.create_hospital_stay()

    def tearDown(self):
        db.cursor.executescript(DROP_TABLES_SCRIPT)
        db.connection.commit()
        db.connection.close()

    def create_doctor(self):
        self.doctor_ID = 1
        self.doctor_name = "Larry"
        self.doctor_lastname = "McGee"
        db.cursor.execute("INSERT INTO doctors (ID, FIRSTNAME, LASTNAME) VALUES (?, ?, ?)",
                   [self.doctor_ID, self.doctor_name, self.doctor_lastname])
        db.connection.commit()

    def create_patient(self):
        self.patient_ID = 1
        self.patient_name = "Mark"
        self.patient_lastname = "Zckbrg"
        self.patient_age = 25
        self.patient_gender = "male"
        db.cursor.execute("INSERT INTO patients (ID, FIRSTNAME, LASTNAME, AGE, GENDER, DOCTOR) VALUES (?, ?, ?, ?, ?, ?)",
                       [self.patient_ID, self.patient_name,
                        self.patient_lastname, self.patient_age,
                        self.patient_gender, self.doctor_ID])
        db.connection.commit()

    def create_hospital_stay(self):
        self.room_id = 205
        self.start_date = "10-10-2010"
        self.end_date = "11-10-2010"
        self.injury = "Schizophrenia"
        db.cursor.execute("""
        INSERT INTO hospital_stay  (ID, ROOM, STARTDATE, ENDDATE, INJURY, PATIENT)
        VALUES (?, ?, ?, ?, ?, ?)""", [
            1, self.room_id, self.start_date, self.end_date, self.injury, self.patient_ID
        ])

    def test_update_patient_age(self):
        new_age = 30
        user_input = "{name}\n{field_to_update}\n{new_value}\n".format(
            name=self.patient_name, field_to_update="age", new_value=new_age
        )
        try:
            sys.stdin = StringIO(user_input)
            sys.stdout = StringIO()
            self.db.update_patient()
            patient = db.cursor.execute("SELECT * FROM PATIENTS").fetchone()
            self.assertEqual(patient['age'], new_age)
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__

    def test_update_invalid_patient(self):
        new_age = 30
        user_input = "{name}\n{field_to_update}\n{new_value}\n".format(
            name="REMY BOYZZ", field_to_update="age", new_value=new_age
        )
        output = StringIO()
        try:
            sys.stdin = StringIO(user_input)
            sys.stdout = output
            self.db.update_patient()
            # assert error message
            self.assertTrue("Such a patient does not exist!" in output.getvalue())
            patient = db.cursor.execute("SELECT * FROM PATIENTS").fetchone()
            self.assertNotEqual(patient['age'], new_age)  # assert that the one patient's name has not changed
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__

    def test_update_doctor_lastname(self):
        new_lastname = "NEWMAN"
        user_input = "{name}\n{field_to_update}\n{new_value}\n".format(
            name=self.doctor_name, field_to_update="lastname", new_value=new_lastname
        )
        try:
            sys.stdin = StringIO(user_input)
            sys.stdout = StringIO()
            self.db.update_doctor()
            doctor = db.cursor.execute("SELECT * FROM DOCTORS").fetchone()
            self.assertEqual(doctor['lastname'], new_lastname)
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__

    def test_update_invalid_doctor(self):
        new_lastname = "NEWMAN"
        user_input = "{name}\n{field_to_update}\n{new_value}\n".format(
            name="INVALID_DOCTOR", field_to_update="lastname", new_value=new_lastname
        )
        output = StringIO()
        try:
            sys.stdin = StringIO(user_input)
            sys.stdout = output
            self.db.update_doctor()
            # assert the error message
            self.assertTrue("Such a doctor does not exist!" in output.getvalue())
            doctor = db.cursor.execute("SELECT * FROM DOCTORS").fetchone()
            # assert that the one doctor's lastname has not change
            self.assertNotEqual(doctor['lastname'], new_lastname)
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__

    def test_update_hospital_stay(self):
        end_date = "20-12-2019"
        user_input = "{name}\n{field_to_update}\n{new_value}\n".format(
            name=self.patient_name, field_to_update="enddate", new_value=end_date
        )
        try:
            sys.stdin = StringIO(user_input)
            sys.stdout = StringIO()
            self.db.update_hospital_stay()
            hospital_stay = db.cursor.execute("SELECT * FROM HOSPITAL_STAY").fetchone()
            self.assertFalse(hospital_stay is None)
            self.assertEqual(hospital_stay['enddate'], end_date)
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__

    def test_update_hospital_stay_invalid_patient(self):
        """ Should just print No such patient and return from the function """
        user_input = "{name}\n".format(
            name="INVALID $ PATIENT")
        output = StringIO()
        try:
            sys.stdin = StringIO(user_input)
            sys.stdout = output
            self.db.update_hospital_stay()
            self.assertTrue("Such a patient does not exist!" in output.getvalue())
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__

    def test_delete_patient(self):
        user_input = "{patient_name}\n".format(
            patient_name=self.patient_name
        )
        try:
            sys.stdin = StringIO(user_input)
            sys.stdout = StringIO()
            self.db.delete_patient()
            # try to get the patient
            patient = db.cursor.execute("SELECT * FROM PATIENTS").fetchone()
            self.assertTrue(patient is None)
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__

    def test_delete_invalid_patient(self):
        user_input = "{patient_name}\n".format(
            patient_name="NOBODY"
        )
        output = StringIO()
        try:
            sys.stdin = StringIO(user_input)
            sys.stdout = output
            self.db.delete_patient()

            # assert there is an error message
            self.assertTrue("Such a patient does not exist!" in output.getvalue())
            # there should be a patient in the db
            patient = db.cursor.execute("SELECT * FROM PATIENTS").fetchone()
            self.assertTrue(patient is not None)
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__

    def test_delete_doctor(self):
        user_input = "{doctor_name}\n".format(
            doctor_name=self.doctor_name)
        try:
            sys.stdin = StringIO(user_input)
            sys.stdout = StringIO()
            self.db.delete_doctor()
            # assert that there are no doctors in the DB
            doctor = db.cursor.execute("SELECT * FROM DOCTORS").fetchone()
            self.assertTrue(doctor is None)
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__

    def test_delete_invalid_doctor(self):
        user_input = "{doctor_name}\n".format(
            doctor_name="INVALID DOC")
        output = StringIO()
        try:
            sys.stdin = StringIO(user_input)
            sys.stdout = output
            self.db.delete_doctor()
            # assert that an error message has been printer
            self.assertTrue("Such a doctor does not exist!" in output.getvalue())
            # assert that there is a doctor in the DB
            doctor = db.cursor.execute("SELECT * FROM DOCTORS").fetchone()
            self.assertTrue(doctor is not None)
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__

    def test_delete_hospital_stay(self):
        user_input = "{patient_name}\n".format(
            patient_name=self.patient_name
        )
        try:
            sys.stdin = StringIO(user_input)
            sys.stdout = StringIO()
            self.db.delete_hospital_stay()
            # assert that the hospital stay is not in the DB
            hospital_stay = db.cursor.execute("SELECT * FROM HOSPITAL_STAY").fetchone()
            self.assertTrue(hospital_stay is None)
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__

    def test_delete_invalid_hospital_stay(self):
        user_input = "{patient_name}\n".format(
            patient_name="Copy paste driven development does not work"
        )
        output = StringIO()
        try:
            sys.stdin = StringIO(user_input)
            sys.stdout = output
            self.db.delete_hospital_stay()
            # assert that an error message has been printer
            self.assertTrue("Such a patient does not exist!" in output.getvalue())
            # assert that the one hospital stay has not been deleted
            hospital_stay = db.cursor.execute("SELECT * FROM HOSPITAL_STAY").fetchone()
            self.assertTrue(hospital_stay is not None)
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__





















if __name__ == '__main__':
    unittest.main()