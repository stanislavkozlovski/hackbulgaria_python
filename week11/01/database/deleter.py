""" All DB Delete actions go here"""
from database.main import conn, cursor
from queries.queries import DELETE_TAN_CODE_BY_TAN_CODE


def delete_tan_code(tan_code):
    cursor.execute(DELETE_TAN_CODE_BY_TAN_CODE, [tan_code])
    conn.commit()
