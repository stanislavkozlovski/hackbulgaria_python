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