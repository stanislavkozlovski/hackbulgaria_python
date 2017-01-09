CREATE_CLIENTS_TABLE = '''create table if not exists
        clients(id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT,
                salt TEXT,
                balance REAL DEFAULT 0,
                message TEXT)'''

CREATE_USER = "INSERT INTO clients (username, password, salt) values (?, ?, ?)"

UPDATE_CLIENT_SET_MESSAGE = "UPDATE clients SET message = ? WHERE id = ?"

UPDATE_CLIENT_SET_PASSWORD = "UPDATE clients SET password = ? WHERE id = ?"

SELECT_ONE_USER_WITH_USERNAME_PASSWORD = "SELECT id, username, balance, message FROM clients WHERE username = ? AND password = ? LIMIT 1"
