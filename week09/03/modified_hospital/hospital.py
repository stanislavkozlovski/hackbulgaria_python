import sqlite3
import queries
import sys
import getpass
import bcrypt
import settings
from validator import validate_password


connection = sqlite3.connect(settings.DB_NAME)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()


def hash_password(password, salt):
    """ Generate a hash using the bcrypt algorithm """
    return bcrypt.hashpw(password, salt)


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


def login_user():
    type_of_login = input("> ")
    while not (type_of_login == '1' or type_of_login == '2'):
        type_of_login = input("> ")

    username = input(">Username\n")
    user = __get_user_by_username(username)
    while not user:
        print("A user with that username does not exist!")
        username = input(">Username\n")
        user = __get_user_by_username(username)

    hashed_password = bcrypt.hashpw(getpass.getpass(prompt=">Password\n"), user['salt'])
    while user.password != hashed_password:
        print("Invalid password!")
        hashed_password = bcrypt.hashpw(getpass.getpass(prompt=">Password\n"), user['salt'])

    if type_of_login == '1':
        pass
    elif type_of_login == '2':
        pass


def login_patient(patient):
    valid_choices = settings.PATIENT_VALID_CHOICES
    menu = settings.PATIENT_MENU_TEXT.format(name=patient['name'])
    print(menu)

    choice = input()
    while choice not in valid_choices:
        print('The valid choices are {}'.format(', '.join(valid_choices)))
        choice = input()
    pass


def see_doctor_academic_title(patient):
    # get the patient's doctor
    doctor = cursor.execute(queries.GET_DOCTOR_BY_ID, [patient['DOCTOR_ID']]).fetchone()
    print("Your Doctor's academic title is {}".format(doctor['academic_title']))


def change_patient_doctor(patient):
    # get the patient's doctor
    doctor = cursor.execute(queries.GET_DOCTOR_BY_ID, [patient['DOCTOR_ID']]).fetchone()
    # show the available doctors
    available_doctors = cursor.execute(queries.GET_ALL_DOCTORS_EXCEPT_NAME, [doctor['username']]).fetchall()
    print("Available doctors to choose: \n\t{doctors}".format(
        doctors = '\n\t'.join(['{idx}) {doctor_name} - {doctor_title}'.format(
            idx=idx, doctor_name=doctor['username'], doctor_title=doctor['academic_title']
        )
            for idx, doctor in enumerate(available_doctors)])
    ))
    # get the choice
    choice = input()
    while not choice.isdigit():
        print('Invalid choice')
        choice = input()
    choice = int(choice)
    while not (0 <= choice < len(available_doctors)):
        print('Invalid choice')
        return change_patient_doctor(patient)
    doctor = available_doctors[choice]

    # update the patient's doctor
    cursor.execute(queries.UPDATE_PATIENT_DOCTOR, [doctor['userId'], patient['id']])


def change_username_or_age(patient):
    print("Type 'username' or 'age' in regards to what you want to change.")
    choice = input()
    while choice not in ['username', 'age']:
        print('Invalid choice!')
        choice = input()

    if choice == 'username':
        new_username = input()
        cursor.execute(queries.UPDATE_PATIENT_USERNAME, [new_username, patient['id']])
        pass
    else:
        # change age
        new_age = input()
        while not new_age.isdigit():
            print('Invalid age!')
            new_age = input()
        cursor.execute(queries.UPDATE_PATIENT_AGE, [new_age, patient['id']])


def register_user():
    username = input(">Username\n")
    password = getpass.getpass(prompt=">Password\n")

    while not validate_password(password):
        print("Your password must be longer than 7 characters "
              "and must contain one uppercase character, one lowercase and one digit!")
        password = getpass.getpass(prompt=">Password\n")

    confirm_password = getpass.getpass(prompt=">Confirm Password\n")

    while password != confirm_password:
        print("Password do not match!")
        confirm_password = getpass.getpass(prompt=">Confirm Password\n")

    age = input(">Your age:\n")
    while not age.isdigit():
        print("Invalid age!")
        age = input(">Your age:\n")

    age = int(age)
    # create a salt for the user and hash his password
    user_salt = bcrypt.gensalt()
    hashed_password = hash_password(password, user_salt)
    user = (username, hashed_password, user_salt, age)

    if settings.DOCTOR_TITLE in username:
        return register_doctor(user)
    else:
        return register_patient(user)


def register_doctor(user: tuple):
    """
    :param user: (username, hashed_password, user_salt, age)
    :return: the Doctor record
    """
    title = input(">Academic title:\n\t{}\n".format(
        '\n\t'.join(settings.DOCTOR_RANKS)
    ))
    while title not in settings.DOCTOR_RANKS:
        print('Invalid title!')
        title = input(">Academic title:\n\t{}\n".format(
            '\n\t'.join(settings.DOCTOR_RANKS)
        ))

    user = __create_user(user)
    doctor = (user[settings.USER_ID_KEY], title)
    doctor = __create_doctor(doctor)
    return doctor


def register_patient(user: tuple):
    """
    :param user: (username, hashed_password, user_salt, age)
    :return:
    """
    doctor_objects = __get_doctors()
    doctors = ["{id}) {name}, {title}".format(
        id=(ids + 1), name=doctor[settings.USER_USERNAME_KEY], title=doctor[settings.DOCTOR_TITLE_KEY])
               for ids, doctor in enumerate(doctor_objects)]
    doctor_choice = input(">Choose a doctor to cure your diseases:\n\t{}\n".format(
        '\n\t'.join(doctors)
    ))
    while not doctor_choice.isdigit() or not (0 < int(doctor_choice) <= len(doctors)):
        print("Invalid Choice!")
        doctor_choice = input(">Choose a doctor to cure your diseases:\n\t{}\n".format(
            '\n\t'.join(doctors)
        ))

    user = __create_user(user)
    user_id = user[settings.USER_ID_KEY]

    doctor_choice = int(doctor_choice) - 1
    doctor_id = doctor_objects[doctor_choice]['doctorId']

    patient = (user_id, doctor_id)
    patient = __create_patient(patient)
    return patient


def __create_user(user: tuple):
    """
    Given a tuple holding the user's information, adds him to the database and returns his record
    """
    # Create the user
    cursor.execute(
        queries.CREATE_USER_RECORD,
        user
    )
    connection.commit()
    # Return the user record
    return __get_user_by_username(user[0])


def __get_user_by_username(username: str):
    return cursor.execute(queries.GET_USER_BY_USERNAME,
                          [username]).fetchone()


def __create_doctor(doctor: tuple):
    """
    Given a tuple holding the doctor's information, add him to the database and return his record
    """
    cursor.execute(queries.CREATE_DOCTOR_RECORD, doctor)
    connection.commit()
    return cursor.execute(queries.GET_DOCTOR_BY_ID,
                          [doctor[0]])


def __create_patient(patient: tuple):
    """
    Given a tuple holding the patient's information, add him to the database and return his record
    """
    cursor.execute(queries.CREATE_PATIENT_RECORD, patient)
    connection.commit()
    return cursor.execute(queries.GET_PATIENT_BY_ID,
                          [patient[0]])


def __get_doctors():
    return cursor.execute(queries.GET_ALL_DOCTORS).fetchall()


def main():
    print("""Welcome to Hospital Manager!
Choose:
1 to Log into the system,
2 to register as a new user,
3 for help main,
4 to exit the system.""")
    create_tables()
    command = input()
    if command == '1':
        pass
    elif command == '2':
        register_user()
    elif command == '3':
        pass
    elif command == '4':
        connection.close()
        sys.exit()


if __name__ == '__main__':
    main()