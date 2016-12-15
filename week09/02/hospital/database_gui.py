import sqlite3
import prettytable
from datetime import datetime
from database_scripts import CREATE_TABLES_SCRIPT
DB_PATH = "new_hospital2.db"


def main():
    create_tables()
    command = input()
    while True:
        command_controller(command)
        command = input()
        if command == 'exit':
            break


def command_controller(command: str):
    AVAILABLE_COMMANDS = {
        # key: name of the command
        # value: the function for the command
        "add_patient": add_patient,
        "add_doctor": add_doctor,
        "add_hospital_stay": add_hospital_stay,
        "update_patient": update_patient,
        "update_doctor": update_doctor,
        "update_hospital_stay": update_hospital_stay
    }
    print("Available commands:\n\t{commands}".format(
        commands="\n\t".join(AVAILABLE_COMMANDS.keys())))

    if command in AVAILABLE_COMMANDS.keys():
        AVAILABLE_COMMANDS[command]()


def list_patients():
    patients = cursor.execute("SELECT * FROM PATIENTS").fetchall()
    if not patients:
        print("There are no patients in the database!")
        return
    patient_keys = patients[0].keys()
    table = prettytable.PrettyTable([key for key in patient_keys])
    for patient in patients:
        table.add_row(patient)
    print(table)


def add_patient():
    patient_name = input(">Patient name: ")
    patient_lastname = input(">Patient lastname: ")
    patient_age = input(">Patient age: ")
    patient_gender = input(">Patient gender (male or female): ")
    cursor.execute("INSERT INTO patients (FIRSTNAME, LASTNAME, AGE, GENDER) VALUES (?, ?, ?, ?)",
                   [patient_name, patient_lastname, patient_age, patient_gender])
    connection.commit()


def update_patient():
    patient_name = input(">Patient's name ")
    patient = _find_patient_by_name(patient_name)
    if not patient:
        print("Such a patient does not exist!")
        return

    field = __get_field_from_user(patient)

    new_value = input("New value: ")
    if new_value.isnumeric():
        new_value = int(new_value)

    cursor.execute("UPDATE PATIENTS SET {} = ? WHERE PATIENTS.FIRSTNAME = ?".format(field),
                   [new_value, patient_name])
    connection.commit()


def delete_patient():
    patient_name = input(">Patient's name ")
    patient = _find_patient_by_name(patient_name)
    if not patient:
        print("Such a patient does not exist!")
        return
    cursor.execute("DELETE FROM PATIENTS WHERE PATIENTS.ID= ?",
                   [patient['id']])
    connection.commit()


def list_doctors():
    doctors = cursor.execute("SELECT * FROM DOCTORS").fetchall()
    if not doctors:
        print("There are no doctors in the database!")
        return
    doctor_keys = doctors[0].keys()
    table = prettytable.PrettyTable([key for key in doctor_keys])
    for doctor in doctors:
        table.add_row(doctor)
    print(table)


def list_patients_of_a_doctor():
    doctor_name = input(">Doctor's name ")
    doctor = _find_doctor_by_name(doctor_name)
    if not doctor:
        print("Such a doctor does not exist!")
        return
    patients = _find_doctor_patients(doctor['id'])
    if not patients:
        print("The doctor has no patients.")
        return
    table = prettytable.PrettyTable([key for key in patients[0].keys()])
    for patient in patients:
        table.add_row(patient)
    print(table)


def list_patients_by_injury():
    groups = cursor.execute("""SELECT hospital_stay.injury , GROUP_CONCAT(patients.firstname)
FROM hospital_stay
JOIN patients
ON patients.id = hospital_stay.patient
GROUP BY hospital_stay.injury;
""").fetchall()

    table = prettytable.PrettyTable([key for key in groups[0].keys()])
    for group in groups:
        table.add_row(group)
    print(table)


def list_doctors_and_injuries_they_treat():
    doctors_and_injuries = cursor.execute("""SELECT hospital_stay.injury , GROUP_CONCAT(doctors.firstname)
FROM hospital_stay
	JOIN patients
	ON patients.id = hospital_stay.patient
		JOIN doctors
		ON patients.doctor = doctors.id
GROUP BY hospital_stay.injury;
""").fetchall()

    table = prettytable.PrettyTable([key for key in doctors_and_injuries[0].keys()])
    for doctor_injury_pair in doctors_and_injuries:
        table.add_row(doctor_injury_pair)
    print(table)


def list_patients_from_to_date():
    start_date = input(">Start date ")
    end_date = input(">End date ")
    # validate the dates
    try:
        if len(start_date) != 10 or len(end_date) != 10:
            print("LEN")
            raise Exception()
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        if start_dt >= end_dt:
            raise Exception()
    except:
        print("Invalid date! (The format must be - yyyy-mm-dd!)")
        return
    patients = cursor.execute("""SELECT patients.*
FROM patients
JOIN hospital_stay
ON hospital_stay.patient = patients.id
WHERE hospital_stay.startdate > ? AND hospital_stay.startdate < ?;""",
                              [start_date, end_date]).fetchall()
    if not patients:
        print("There are no patients in that timeframe.")
        return
    table = prettytable.PrettyTable([key for key in patients[0].keys()])
    for patient in patients:
        table.add_row(patient)
    print(table)


def add_doctor():
    doctor_name = input(">Doctor name: ")
    doctor_lastname = input(">Doctor lastname: ")
    cursor.execute("INSERT INTO doctors (FIRSTNAME, LASTNAME) VALUES (?, ?)",
                   [doctor_name, doctor_lastname])
    connection.commit()


def update_doctor():
    doctor_name = input(">Doctor's name ")
    doctor = _find_doctor_by_name(doctor_name)
    if not doctor:
        print("Such a doctor does not exist!")
        return

    field = __get_field_from_user(doctor)

    new_value = input("New value: ")
    if new_value.isnumeric():
        new_value = int(new_value)

    cursor.execute("UPDATE DOCTORS SET {} = ? WHERE DOCTORS.FIRSTNAME = ?".format(field),
                   [new_value, doctor_name])
    connection.commit()


def delete_doctor():
    doctor_name = input(">Doctor's name ")
    doctor = _find_doctor_by_name(doctor_name)
    if not doctor:
        print("Such a doctor does not exist!")
        return
    cursor.execute("DELETE FROM DOCTORS WHERE DOCTORS.ID = ?",
                   [doctor['id']])
    connection.commit()


def add_hospital_stay():
    patient_name = input(">Patient's name ")
    patient = _find_patient_by_name(patient_name)
    if not patient:
        print("Such a patient does not exist!")
        return

    room = int(input(">Room number: "))
    start_date = input(">Entry date: ")
    end_date = input(">Exit date: (leave blank if still in)") or None
    injury = input(">Enter the reason for the stay: ")
    cursor.execute("INSERT INTO hospital_stay (ROOM, STARTDATE, ENDDATE, INJURY, PATIENT) VALUES (?, ?, ?, ?, ?)",
                   [room, start_date, end_date, injury, patient[0]])
    connection.commit()


def update_hospital_stay():
    patient_name = input(">Patient's name ")
    patient = _find_patient_by_name(patient_name)
    if not patient:
        print("Such a patient does not exist!")
        return
    hospital_stay = _find_hospital_stay_by_patient_id(patient['id'])
    if not hospital_stay:
        print("There are no records for the patient staying in the hospital.")
        return
    field = __get_field_from_user(hospital_stay)
    new_value = input("New value: ")
    if new_value.isnumeric():
        new_value = int(new_value)

    cursor.execute("UPDATE HOSPITAL_STAY SET {} = ? WHERE HOSPITAL_STAY.ID = ?".format(field),
                   [new_value, hospital_stay['id']])
    connection.commit()


def delete_hospital_stay():
    patient_name = input(">Patient's name ")
    patient = _find_patient_by_name(patient_name)
    if not patient:
        print("Such a patient does not exist!")
        return
    hospital_stay = _find_hospital_stay_by_patient_id(patient['id'])
    if not hospital_stay:
        print("There are no records for the patient staying in the hospital.")
        return

    cursor.execute("DELETE FROM HOSPITAL_STAY WHERE HOSPITAL_STAY.ID = ?",
                   [hospital_stay['id']])
    connection.commit()


def _find_patient_by_name(patient_name):
    return cursor.execute("SELECT * FROM patients WHERE patients.firstName = ?", [patient_name]).fetchone()


def _find_doctor_by_name(doctor_name):
    return cursor.execute("SELECT * FROM doctors WHERE doctors.firstName = ?",
                          [doctor_name]).fetchone()


def _find_doctor_patients(doctor_id):
    return cursor.execute("SELECT * FROM patients WHERE patients.doctor = ?",
                          [doctor_id]).fetchall()


def _find_hospital_stay_by_patient_id(patient_id):
    return cursor.execute("SELECT * FROM hospital_stay WHERE hospital_stay.patient = ?",
                          [patient_id]).fetchone()


def __get_field_from_user(row_object: sqlite3.Row):
    """
    Prompts the user to enter the field he wants to update,
    listing the available fields from the object
    """
    print("Pick a field to update: \n\t{fields}".format(
        fields='\n\t'.join(row_object.keys())
    ))
    field = input().upper()
    while field not in row_object.keys():
        print("Invalid key!")
        field = input().upper()
    return field


def create_tables():
    cursor.executescript(CREATE_TABLES_SCRIPT)
    connection.commit()
    print("TABLES CREATED!")


if __name__ == '__main__':
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    try:
        cursor = connection.cursor()
        main()
    finally:
        connection.close()