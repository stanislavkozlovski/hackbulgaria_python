import bcrypt
import sqlite3
from queries.queries import (CREATE_CLIENTS_TABLE, UPDATE_CLIENT_SET_MESSAGE, UPDATE_CLIENT_SET_PASSWORD,
                            CREATE_USER, SELECT_ONE_USER_WITH_USERNAME_PASSWORD, GET_USER_PASSWORD_BY_USERNAME)
from client import Client
from settings.constants import (DB_PATH, DB_USER_ID_KEY, DB_USER_USERNAME_KEY, DB_USER_BALANCE_KEY,
                                DB_USER_MESSAGE_KEY)
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()


def create_clients_table():
    cursor.execute(CREATE_CLIENTS_TABLE)


def change_message(new_message, logged_user):
    cursor.execute(UPDATE_CLIENT_SET_MESSAGE, (new_message, logged_user.id))
    conn.commit()
    logged_user.message = new_message


def change_pass(new_pass, logged_user):
    # hash the password
    user_salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(new_pass, user_salt)
    cursor.execute(UPDATE_CLIENT_SET_PASSWORD, (hashed_password, logged_user.id))
    conn.commit()


def register(username, password):
    # hash the password
    user_salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), user_salt)
    cursor.execute(CREATE_USER, (username, hashed_password))
    conn.commit()


def login(username, password):
    # hash the password
    user_salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), user_salt)
    cursor.execute(SELECT_ONE_USER_WITH_USERNAME_PASSWORD, (username, hashed_password))
    user = cursor.fetchone()

    if user:
        return Client(_id=user[DB_USER_ID_KEY],
                      username=user[DB_USER_USERNAME_KEY],
                      balance=user[DB_USER_BALANCE_KEY],
                      message=user[DB_USER_MESSAGE_KEY])
    else:
        return False
