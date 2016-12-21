DB_NAME = 'modified_hospital.db'
DOCTOR_TITLE = 'Dr.'
DOCTOR_RANKS = ['student', 'intern', 'apprentice', 'journeyman', 'experienced', 'master']

USER_ID_KEY = 'id'
USER_USERNAME_KEY = 'username'

DOCTOR_TITLE_KEY = 'academic_title'

MAIN_CHOICE_LOG_IN_KEY = '1'
MAIN_CHOICE_REGISTER_KEY = '2'
MAIN_CHOICE_HELP_KEY = '3'
MAIN_CHOICE_EXIT_KEY = '4'

PATIENT_MENU_TEXT = """Hi, {name},
You are a patient in Hospital Manager.
You have the abilities to:
1) see the free hours of your doctor
2) reserve hour for visitation
3) stay at the hospital for an injury
4) see the academic title of his doctor
5) list your hospital stays
6) change your doctor
7) change your username and/or age
8) log out"""
PATIENT_VALID_CHOICES = ['1', '2', '3', '4', '5', '6', '7', '8']
