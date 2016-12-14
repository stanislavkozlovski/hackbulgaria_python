import sqlite3
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
    if command == "add_patient":
        add_patient()
    pass


def add_patient():
    patient_name = input(">Patient name: ")
    patient_lastname = input(">Patient lastname: ")
    patient_age = input(">Patient age: ")
    patient_gender = input(">Patient gender (male or female): ")
    cursor.execute("INSERT INTO patients (FIRSTNAME, LASTNAME, AGE, GENDER) VALUES (?, ?, ?, ?)",
                   [patient_name, patient_lastname, patient_age, patient_gender])
    connection.commit()


def add_doctor():
    doctor_name = input(">Doctor name: ")
    doctor_lastname = input(">Doctor lastname: ")
    cursor.execute("INSERT INTO doctors (FIRSTNAME, LASTNAME) VALUES (?, ?)",
                   [doctor_name, doctor_lastname])
    connection.commit()


def add_hospital_stay():
    patient_name = input(">Patient's name ")
    patient = cursor.execute("SELECT * FROM patients WHERE patients.firstName = ?", [patient_name]).fetchone()
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


def create_tables():
    cursor.executescript(CREATE_TABLES_SCRIPT)
    connection.commit()
    print("TABLES CREATED!")


if __name__ == '__main__':
    connection = sqlite3.connect(DB_PATH)
    try:
        cursor = connection.cursor()
        main()
    finally:
        connection.close()