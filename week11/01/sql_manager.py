import bcrypt
import sqlite3
import dateutil.parser as dateparser
from datetime import datetime
from queries.queries import (CREATE_CLIENTS_TABLE, UPDATE_CLIENT_SET_MESSAGE, UPDATE_CLIENT_SET_PASSWORD,
                            CREATE_USER, SELECT_ONE_USER_WITH_USERNAME_PASSWORD, CREATE_INVALID_LOGINS_TABLE,
                             CREATE_INVALID_LOGINS_USER, SELECT_USER_ID_BY_USERNAME, SELECT_INVALID_LOGINS,
                             UPDATE_INVALID_LOGINS_SET_INVALID_LOGIN_COUNT, SELECT_USER_LAST_BLOCKED_BY_USERNAME,
                             UPDATE_CLIENT_LAST_BLOCKED)
from client import Client
from settings.constants import (DB_PATH, DB_USER_ID_KEY, DB_USER_USERNAME_KEY, DB_USER_BALANCE_KEY,
                                DB_USER_MESSAGE_KEY, DB_INVALID_LOGINS_INVALID_LOGIN_COUNT_KEY, DB_ID_KEY,
                                DB_USER_LAST_BLOCKED_KEY, INVALID_LOGIN_BRUTEFORCE_PROTECTION_COUNT)
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()


def create_clients_table():
    cursor.execute(CREATE_CLIENTS_TABLE)
    cursor.execute(CREATE_INVALID_LOGINS_TABLE)


def get_user_salt(username):
    salt = cursor.execute('SELECT salt FROM clients WHERE username=?', [username]).fetchone()
    if salt is not None:
        return salt[0]


def get_user_id(username):
    id = cursor.execute(SELECT_USER_ID_BY_USERNAME, [username]).fetchone()
    if id is not None:
        return id[0]


def get_invalid_login(_id):
    invalid_login = cursor.execute(SELECT_INVALID_LOGINS, [_id]).fetchone()
    return invalid_login


def change_message(new_message, logged_user):
    cursor.execute(UPDATE_CLIENT_SET_MESSAGE, (new_message, logged_user.id))
    conn.commit()
    logged_user.message = new_message


def change_pass(new_pass, logged_user):
    # hash the password
    user_salt = get_user_salt(logged_user.username)
    hashed_password = bcrypt.hashpw(new_pass.encode(), user_salt)
    cursor.execute(UPDATE_CLIENT_SET_PASSWORD, (hashed_password, logged_user.id))
    conn.commit()


def register(username, password, email):
    # hash the password
    user_salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), user_salt)
    cursor.execute(CREATE_USER, (username, hashed_password, user_salt, email))
    # get the user's id
    id = get_user_id(username)
    cursor.execute(CREATE_INVALID_LOGINS_USER, [id])
    conn.commit()


def login(username, password):
    # check if the username is valid
    user_id = get_user_id(username)
    if user_id is None:
        return False
    last_blocked = get_last_blocked(username)
    if last_blocked and (datetime.now() - dateparser.parse(last_blocked)).seconds < 300:
        # user is blocked for 5 minutes
        return False
    # hash the password
    user_salt = get_user_salt(username)
    hashed_password = bcrypt.hashpw(password.encode(), user_salt)
    cursor.execute(SELECT_ONE_USER_WITH_USERNAME_PASSWORD, (username, hashed_password))
    user = cursor.fetchone()

    if user:
        # successful login, reset the invalid_logins table
        reset_invalid_logins(user_id)
        return Client(_id=user_id,
                      username=user[DB_USER_USERNAME_KEY],
                      balance=user[DB_USER_BALANCE_KEY],
                      message=user[DB_USER_MESSAGE_KEY])
    else:
        if user_id is not None:
            # invalid login, must increment in the DB table
            invalid_login = get_invalid_login(user_id)
            invalid_login_count = invalid_login[DB_INVALID_LOGINS_INVALID_LOGIN_COUNT_KEY] + 1
            if invalid_login_count == INVALID_LOGIN_BRUTEFORCE_PROTECTION_COUNT:
                # block user
                block_user(user_id)
            else:
                increment_invalid_logins(invalid_login[DB_ID_KEY])
        return False


def get_last_blocked(username):
    """ Get the time the user was last blocked """
    last_blocked = cursor.execute(SELECT_USER_LAST_BLOCKED_BY_USERNAME, [username]).fetchone()
    if last_blocked is not None:
        return last_blocked[DB_USER_LAST_BLOCKED_KEY]


def reset_invalid_logins(_id):
    """ Reset the invalid logins count for a user"""
    invalid_logins = get_invalid_login(_id)
    if invalid_logins is None:
        raise Exception('Invalid user id!')

    cursor.execute(UPDATE_INVALID_LOGINS_SET_INVALID_LOGIN_COUNT, [0, invalid_logins[DB_ID_KEY]])
    conn.commit()


def increment_invalid_logins(_id):
    """ Increment the invalid logins count for a user """
    invalid_logins = get_invalid_login(_id)
    if invalid_logins is None:
        raise Exception('Invalid user id!')
    invalid_logins_count = invalid_logins[DB_INVALID_LOGINS_INVALID_LOGIN_COUNT_KEY] + 1
    cursor.execute(UPDATE_INVALID_LOGINS_SET_INVALID_LOGIN_COUNT, [invalid_logins_count, invalid_logins[DB_ID_KEY]])
    conn.commit()


def block_user(user_id):
    time_now = str(datetime.now())
    cursor.execute(UPDATE_CLIENT_LAST_BLOCKED, [time_now, user_id])
    conn.commit()
