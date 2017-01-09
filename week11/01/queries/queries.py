CREATE_CLIENTS_TABLE = '''create table if not exists
        clients(id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT,
                salt TEXT,
                email TEXT,
                balance REAL DEFAULT 0,
                message TEXT,
                last_blocked TEXT)'''

CREATE_INVALID_LOGINS_TABLE = '''CREATE TABLE IF NOT EXISTS
    invalid_logins(id INTEGER PRIMARY KEY,
                   login_count INTEGER,
                    FOREIGN KEY(ID) REFERENCES USER(ID))'''

CREATE_USER = "INSERT INTO clients (username, password, salt, email) values (?, ?, ?, ?)"

CREATE_INVALID_LOGINS_USER = "INSERT INTO invalid_logins (id, login_count) values (?, 0)"

SELECT_INVALID_LOGINS = "SELECT * FROM invalid_logins WHERE id = ?"

UPDATE_INVALID_LOGINS_SET_INVALID_LOGIN_COUNT = "UPDATE invalid_logins SET login_count = ? WHERE id = ?"

UPDATE_CLIENT_SET_MESSAGE = "UPDATE clients SET message = ? WHERE id = ?"

UPDATE_CLIENT_SET_PASSWORD = "UPDATE clients SET password = ? WHERE id = ?"

UPDATE_CLIENT_LAST_BLOCKED = "UPDATE clients SET last_blocked = ? WHERE id = ?"

SELECT_ONE_USER_WITH_USERNAME_PASSWORD = "SELECT id, username, email, salt, balance, message FROM clients WHERE username = ? AND password = ? LIMIT 1"

SELECT_USER_ID_BY_USERNAME = "SELECT id FROM clients WHERE username = ?"

SELECT_USER_LAST_BLOCKED_BY_USERNAME = 'SELECT last_blocked FROM clients WHERE username = ?'
