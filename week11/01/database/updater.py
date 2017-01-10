""" Update calls to the DB go here """
from database.main import conn, cursor
from queries.queries import (UPDATE_CLIENT_RESET_TOKEN, UPDATE_CLIENT_SET_PASSWORD, UPDATE_CLIENT_LAST_BLOCKED,
                             UPDATE_INVALID_LOGINS_SET_INVALID_LOGIN_COUNT)


def update_user_password_reset_token(user_id, reset_token):
    cursor.execute(UPDATE_CLIENT_RESET_TOKEN, [reset_token, user_id])
    conn.commit()


def update_user_password(user_id, new_password):
    cursor.execute(UPDATE_CLIENT_SET_PASSWORD, (new_password, user_id))
    conn.commit()


def update_user_last_blocked(user_id, time_of_block):
    cursor.execute(UPDATE_CLIENT_LAST_BLOCKED, [time_of_block, user_id])
    conn.commit()


def update_invalid_login_login_count(invalid_login_id, invalid_login_count):
    cursor.execute(UPDATE_INVALID_LOGINS_SET_INVALID_LOGIN_COUNT, [invalid_login_count, invalid_login_id])
    conn.commit()
