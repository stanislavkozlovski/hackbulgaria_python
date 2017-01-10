""" All DB create operations go here """
from typing import Iterable

from database.main import conn, cursor
from queries.queries import CREATE_TAN_CODE


def create_tan_codes(user_id, tan_codes: Iterable):
    tan_codes = [(user_id, str(code)) for code in tan_codes]
    cursor.executemany(CREATE_TAN_CODE, tan_codes)
    conn.commit()
