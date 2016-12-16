import sqlite3
from settings import DB_NAME
import queries
import sys

connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()


def create_tables(drop_old=False):
    if drop_old:
        cursor.executescript(
            queries.DROP_DOCTOR_TABLE + queries.DROP_HOSPITAL_STAY_TABLE
            + queries.DROP_PATIENT_TABLE + queries.DROP_USER_TABLE
            + queries.DROP_VISITATION_TABLE
        )

    cursor.executescript(
        queries.CREATE_USER_TABLE + queries.CREATE_DOCTOR_TABLE
        + queries.CREATE_HOSPITAL_STAY_TABLE + queries.CREATE_PATIENT_TABLE
        + queries.CREATE_VISITATION_TABLE
    )
    connection.commit()


def register_user():
    username = input(">Username\n")
    password = input(">Password\n")
    confirm_password = input(">Confirm Password\n")


def main():
    print("""Welcome to Hospital Manager!
Choose:
1 to Log into the system,
2 to register as a new user,
3 for help main,
4 to exit the system.""")
    command = input()
    if command == '1':
        pass
    elif command == '2':
        pass
    elif command == '3':
        pass
    elif command == '4':
        sys.exit()



if __name__ == '__main__':
    main()