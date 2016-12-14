import sqlite3
from database_scripts import CREATE_TABLES_SCRIPT
DB_PATH = "new_hospital2.db"


def main():
    create_tables()
    command = input()
    while True:
        command_controller(command)
        command = input()
        if command == 'exit':
            break


def command_controller(command: str):
    pass


def create_tables():
    cursor.executescript(CREATE_TABLES_SCRIPT)
    connection.commit()
    print("TABLES CREATED!")


if __name__ == '__main__':
    connection = sqlite3.connect(DB_PATH)
    try:
        cursor = connection.cursor()
        main()
    finally:
        connection.close()