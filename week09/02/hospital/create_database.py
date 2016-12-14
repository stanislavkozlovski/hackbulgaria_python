import sqlite3

DB_NAME = "new_hospital2.db"

db = sqlite3.connect(DB_NAME)
db.row_factory = sqlite3.Row

drop_databases = """----- Tables -----
DROP TABLE IF EXISTS PATIENT;
DROP TABLE IF EXISTS HOSPITAL_STAY;
DROP TABLE IF EXISTS DOCTORS;"""
cursor = db.cursor()

cursor.executescript(drop_databases)
db.commit()

create_patients_table = """
CREATE TABLE IF NOT EXISTS PATIENT
(
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  FIRSTNAME TEXT NOT NULL,
  LASTNAME TEXT NOT NULL,
  AGE int NOT NULL
);"""

cursor.execute(create_patients_table)
db.commit()

insert_patient = """
INSERT INTO PATIENT (FIRSTNAME, LASTNAME, AGE)
VALUES(?, ?, ?)"""

cursor.execute(insert_patient, ["Viktor", "Barzin", 18])
db.commit()


patients = [
    ("Stanislav", "Kozlovski", 20),
    ("Zen", "Man", 40),
    ("Tsetsi", "Man", 14)
]


cursor.executemany(insert_patient, patients)
db.commit()

list_patients = """
SELECT *
FROM PATIENT
"""

results = cursor.execute(list_patients).fetchall()
print(results[0]['firstname'])
