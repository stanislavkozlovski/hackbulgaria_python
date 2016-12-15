import sqlite3
import prettytable
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