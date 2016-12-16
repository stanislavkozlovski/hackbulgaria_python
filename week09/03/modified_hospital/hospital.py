import sqlite3
import queries
import sys
import getpass
import hashlib, uuid


from settings import DB_NAME, DOCTOR_TITLE
from validator import validate_password


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
    password = getpass.getpass(prompt=">Password\n")

    while not validate_password(password):
        print("Your password must be longer than 7 characters "
              "and must contain one uppercase character, one lowercase and one digit!")
        password = getpass.getpass(prompt=">Password\n")

    confirm_password = getpass.getpass(prompt=">Password\n")

    while password != confirm_password:
        print("Password do not match!")
        confirm_password = getpass.getpass(prompt=">Confirm Password\n")

    age = input(">Your age:\n")
    while not age.isdigit():
        print("Invalid age!")
        age = input(">Your age:\n")

    age = int(age)
    # create a salt for the user and hash his password
    user_salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512(password + user_salt).hexdigest()
    user = (username, hashed_password, user_salt, age)

    if DOCTOR_TITLE in username:
        return register_doctor(user)
    else:
        return register_patient(user)


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
        register_user()
    elif command == '3':
        pass
    elif command == '4':
        sys.exit()


if __name__ == '__main__':
    main()