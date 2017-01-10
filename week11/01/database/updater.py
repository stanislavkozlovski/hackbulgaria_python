""" Update calls to the DB go here """
from sql_manager import conn, cursor
from queries.queries import UPDATE_CLIENT_RESET_TOKEN


def update_user_password_reset_token(user_id, reset_token):
    cursor.execute(UPDATE_CLIENT_RESET_TOKEN, [reset_token, user_id])
    conn.commit()
