import bcrypt
import dateutil.parser as dateparser
from datetime import datetime
from queries.queries import (CREATE_CLIENTS_TABLE, UPDATE_CLIENT_SET_MESSAGE, UPDATE_CLIENT_SET_PASSWORD,
                             CREATE_USER, SELECT_ONE_USER_WITH_USERNAME_PASSWORD, CREATE_INVALID_LOGINS_TABLE,
                             CREATE_INVALID_LOGINS_USER, SELECT_USER_ID_BY_USERNAME, SELECT_INVALID_LOGINS,
                             UPDATE_INVALID_LOGINS_SET_INVALID_LOGIN_COUNT, SELECT_USER_LAST_BLOCKED_BY_USERNAME,
                             UPDATE_CLIENT_LAST_BLOCKED, SELECT_ONE_USER_WITH_USERNAME, UPDATE_CLIENT_RESET_TOKEN,
                             CREATE_TAN_CODES_TABLE)
from database.reader import fetch_user_salt, fetch_user_id, fetch_invalid_login, fetch_user_tan_codes
from database.updater import update_user_password, update_user_last_blocked, update_invalid_login_login_count
from client import Client
from settings.constants import (DB_PATH, DB_USER_ID_KEY, DB_USER_USERNAME_KEY, DB_USER_BALANCE_KEY,
                                DB_USER_MESSAGE_KEY, DB_INVALID_LOGINS_INVALID_LOGIN_COUNT_KEY, DB_ID_KEY,
                                DB_USER_LAST_BLOCKED_KEY, INVALID_LOGIN_BRUTEFORCE_PROTECTION_COUNT, DB_USER_EMAIL_KEY,
                                DB_TAN_CODES_TAN_CODE_KEY)
from database.main import cursor, conn


def create_tables():
    cursor.execute(CREATE_CLIENTS_TABLE)
    cursor.execute(CREATE_INVALID_LOGINS_TABLE)
    cursor.execute(CREATE_TAN_CODES_TABLE)


def change_message(new_message, logged_user):
    cursor.execute(UPDATE_CLIENT_SET_MESSAGE, (new_message, logged_user.id))
    conn.commit()
    logged_user.message = new_message


def change_pass(new_pass, logged_user):
    user_salt = fetch_user_salt(logged_user.username)
    hashed_password = bcrypt.hashpw(new_pass.encode(), user_salt)
    update_user_password(logged_user.id, hashed_password)


def register(username, password, email):
    # hash the password
    user_salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), user_salt)
    cursor.execute(CREATE_USER, (username, hashed_password, user_salt, email))
    # get the user's id
    id = fetch_user_id(username)
    cursor.execute(CREATE_INVALID_LOGINS_USER, [id])
    conn.commit()


def login(username, password):
    # check if the username is valid
    user_id = fetch_user_id(username)
    if user_id is None:
        return False
    last_blocked = get_last_blocked(username)
    if last_blocked and (datetime.now() - dateparser.parse(last_blocked)).seconds < 300:
        # user is blocked for 5 minutes
        return False
    # hash the password
    user_salt = fetch_user_salt(username)
    hashed_password = bcrypt.hashpw(password.encode(), user_salt)
    cursor.execute(SELECT_ONE_USER_WITH_USERNAME_PASSWORD, (username, hashed_password))
    user = cursor.fetchone()

    if user:
        # successful login, reset the invalid_logins table
        reset_invalid_logins(user_id)

        tan_codes = [row[DB_TAN_CODES_TAN_CODE_KEY] for row in fetch_user_tan_codes(user_id)]
        return Client(_id=user_id,
                      username=user[DB_USER_USERNAME_KEY],
                      email=user[DB_USER_EMAIL_KEY],
                      tan_codes=tan_codes,
                      balance=user[DB_USER_BALANCE_KEY],
                      message=user[DB_USER_MESSAGE_KEY])
    else:
        if user_id is not None:
            # invalid login, must increment in the DB table
            invalid_login = fetch_invalid_login(user_id)
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
    invalid_logins = fetch_invalid_login(_id)
    if invalid_logins is None:
        raise Exception('Invalid user id!')

    cursor.execute(UPDATE_INVALID_LOGINS_SET_INVALID_LOGIN_COUNT, [0, invalid_logins[DB_ID_KEY]])
    conn.commit()


def reset_user_password_reset_token(user):
    cursor.execute(UPDATE_CLIENT_RESET_TOKEN, ['', user[DB_ID_KEY]])
    conn.commit()


def increment_invalid_logins(_id):
    """ Increment the invalid logins count for a user """
    invalid_logins = fetch_invalid_login(_id)
    if invalid_logins is None:
        raise Exception('Invalid user id!')
    invalid_logins_count = invalid_logins[DB_INVALID_LOGINS_INVALID_LOGIN_COUNT_KEY] + 1
    update_invalid_login_login_count(invalid_logins[DB_ID_KEY], invalid_logins_count)


def block_user(user_id):
    time_of_block = str(datetime.now())
    update_user_last_blocked(user_id, time_of_block)
