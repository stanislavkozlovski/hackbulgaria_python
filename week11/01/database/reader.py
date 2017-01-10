""" All DB read operations go here """
from database.main import conn, cursor
from queries.queries import (SELECT_ONE_USER_WITH_USERNAME, SELECT_USER_ID_BY_USERNAME,
                             SELECT_INVALID_LOGINS, SELECT_USER_PASSWORD_RESET_TOKEN, SELECT_USER_BALANCE)


def fetch_user_by_name(username):
    user = cursor.execute(SELECT_ONE_USER_WITH_USERNAME, [username]).fetchone()
    return user


def fetch_user_salt(username):
    salt = cursor.execute('SELECT salt FROM clients WHERE username=?', [username]).fetchone()
    if salt is not None:
        return salt[0]


def fetch_user_id(username):
    id = cursor.execute(SELECT_USER_ID_BY_USERNAME, [username]).fetchone()
    if id is not None:
        return id[0]


def fetch_user_balance(username):
    balance = cursor.execute(SELECT_USER_BALANCE, [username]).fetchone()
    if balance is not None:
        return balance[0]


def fetch_user_password_reset_token(username):
    reset_token = cursor.execute(SELECT_USER_PASSWORD_RESET_TOKEN, [username]).fetchone()
    if reset_token is not None:
        return reset_token[0]


def fetch_invalid_login(_id):
    invalid_login = cursor.execute(SELECT_INVALID_LOGINS, [_id]).fetchone()
    return invalid_login
