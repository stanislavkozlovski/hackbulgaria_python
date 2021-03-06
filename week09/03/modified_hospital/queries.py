DROP_USER_TABLE = '''
    DROP TABLE IF EXISTS USER;
'''

DROP_PATIENT_TABLE = '''
    DROP TABLE IF EXISTS PATIENT;
'''

DROP_DOCTOR_TABLE = '''
    DROP TABLE IF EXISTS DOCTOR;
'''

DROP_HOSPITAL_STAY_TABLE = '''
    DROP TABLE IF EXISTS HOSPITAL_STAY;
'''

DROP_VISITATION_TABLE = '''
    DROP TABLE IF EXISTS VISITATION;
'''


CREATE_USER_TABLE = '''
    CREATE TABLE IF NOT EXISTS User (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        USERNAME TEXT NOT NULL,
        PASSWORD TEXT NOT NULL,
        SALT TEXT NOT NULL,
        IS_ACTIVE INTEGER NOT NULL DEFAULT 0,
        AGE INTEGER
    );
'''

CREATE_DOCTOR_TABLE = '''
    CREATE TABLE IF NOT EXISTS DOCTOR (
        ID INTEGER PRIMARY KEY,
        ACADEMIC_TITLE TEXT,
        FOREIGN KEY (ID) REFERENCES USER(ID)
    );
'''

CREATE_PATIENT_TABLE = '''
    CREATE TABLE IF NOT EXISTS PATIENT (
        ID INTEGER PRIMARY KEY,
        DOCTOR_ID INTEGER,
        FOREIGN KEY (ID) REFERENCES USER(ID),
        FOREIGN KEY (DOCTOR_ID) REFERENCES DOCTOR(ID)
    );
'''

CREATE_HOSPITAL_STAY_TABLE = '''
    CREATE TABLE IF NOT EXISTS HOSPITAL_STAY (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        STARTDATE TEXT NOT NULL,
        ENDDATE TEXT,
        ROOM INTEGER NOT NULL,
        INJURY TEXT NOT NULL,
        PATIENT_ID INTEGER,
        FOREIGN KEY (PATIENT_ID) REFERENCES PATIENT(ID)
    );
'''

CREATE_VISITATION_TABLE = '''
    CREATE TABLE IF NOT EXISTS VISITATION (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        PATIENT_ID INTEGER,
        DOCTOR_ID INTEGER NOT NULL,
        START_HOUR TEXT NOT NULL,
        FOREIGN KEY (PATIENT_ID) REFERENCES PATIENT(ID),
        FOREIGN KEY (DOCTOR_ID) REFERENCES DOCTOR(ID)
    );
'''

CREATE_USER_RECORD = '''
    INSERT INTO user (USERNAME, PASSWORD, SALT, AGE)
    VALUES (?, ?, ?, ?);
'''


CREATE_DOCTOR_RECORD = '''
    INSERT INTO doctor (ID, ACADEMIC_TITLE)
    VALUES (?, ?);
'''

CREATE_PATIENT_RECORD = '''
    INSERT INTO patient (ID, DOCTOR_ID)
    VALUES (?, ?);
'''


GET_USER_BY_USERNAME = '''
    SELECT *
    FROM user
    WHERE username = ?;
'''

GET_DOCTOR_BY_ID = '''
    SELECT user.username, user.age, user.id as userId, doctor.id as doctorId, doctor.academic_title
    FROM doctor
    JOIN user
    ON user.id = doctor.id
    WHERE doctor.id = ?;
'''

GET_PATIENT_BY_ID = '''
    SELECT user.username, user.age, user.id as userId, patient.doctor_id
    FROM patient
    JOIN user
    ON user.id = patient.id
    WHERE patient.id = ?;
'''

GET_ALL_DOCTORS = '''
    SELECT user.username, user.age, user.id as userId, doctor.id as doctorId, doctor.academic_title
    FROM doctor
    JOIN user
    ON user.id = doctor.id;
'''

GET_ALL_DOCTORS_EXCEPT_NAME = '''
SELECT user.username, user.age, user.id as userId, doctor.id as doctorId, doctor.academic_title
    FROM doctor
    JOIN user
    ON user.id = doctor.id
    WHERE user.username != ?;
'''

UPDATE_PATIENT_USERNAME = '''
UPDATE user
SET username = ?
WHERE user.id = ?'''

UPDATE_PATIENT_AGE = '''
UPDATE user
SET age = ?
WHERE user.id = ?'''

UPDATE_PATIENT_DOCTOR = '''
UPDATE patient
SET doctor_id = ?
WHERE patient.id = ?;'''