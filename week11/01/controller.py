import bcrypt
from settings.constants import INVALID_LOGIN_BRUTEFORCE_PROTECTION_COUNT, TAN_CODE_COUNT_PER_GENERATION as MAX_TAN_CODE_COUNT
from database.main import session
from database.models import Client, InvalidLogin, TanCode
from dateutil import parser as dateparser
from datetime import datetime
from utils.tan_codes import send_email, send_tan_codes, generate_tan_codes
import atexit


def register(username, password, email):
    # hash the password
    user_salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), user_salt)
    new_user = Client(username=username, password=hashed_password, salt=user_salt, email=email)
    session.add(new_user)
    session.commit()  # to save the user and id
    invalid_logins = InvalidLogin(id_=new_user.id_, login_count=0)
    session.add(invalid_logins)
    session.flush()
    session.commit()


def change_password(user, password):
    user_salt = user.salt
    hashed_password = bcrypt.hashpw(password.encode(), user_salt)
    user.password = hashed_password
    session.commit()


def login(username, password):
    # check if the username is valid
    orig_user = session.query(Client).filter_by(username=username).one_or_none()
    if orig_user is None:
        return False
    last_blocked = orig_user.last_blocked
    if last_blocked and (datetime.now() - dateparser.parse(last_blocked)).seconds < 300:
        # user is blocked for 5 minutes
        return False
    # hash the password
    user_salt = orig_user.salt
    hashed_password = bcrypt.hashpw(password.encode(), user_salt)
    user = session.query(Client).filter_by(username=username, password=hashed_password).one_or_none()

    if user:
        # successful login, reset the invalid_logins table
        user.invalid_logins.login_count = 0

        return user
    else:
        if orig_user is not None:
            # invalid login, must increment in the DB table
            invalid_login_count = orig_user.invalid_logins.login_count + 1
            if invalid_login_count == INVALID_LOGIN_BRUTEFORCE_PROTECTION_COUNT:
                # block user
                block_user(orig_user)
            else:
                orig_user.invalid_logins.login_count = invalid_login_count

        return False


def block_user(user):
    time_of_block = str(datetime.now())
    user.last_blocked = time_of_block


def is_valid_tan_code(user, tan_code: str):
    return tan_code in [tc.tan_code for tc in user.tan_codes]


def deposit_money(user, amount):
    user.balance += amount


def consume_tan_code(tan_code):
    t_code = session.query(TanCode).filter_by(tan_code=tan_code)
    t_code.delete(synchronize_session='fetch')
    session.flush()
    session.commit()


def withdraw_money(user, amount: float):
    if user.balance < amount:
        print('You cannot withdraw more money than you have!')
        return False
    user.balance -= amount

    return True


def generate_tan_codes(user):
    if len(user.tan_codes) == 0:
        tan_codes, success = send_tan_codes(user.email)
        # if not success:
        #     print('Something went wrong when creating your TAN codes.')
        #     return
        # self.__tan_codes = tan_codes
        tan_codes_to_save = []
        for tan_code in tan_codes:
            tan_codes_to_save.append(TanCode(user_id=user.id_, tan_code=tan_code))
        session.add_all(tan_codes_to_save)
        session.flush()
        session.commit()
    else:
        print('You still have {} TAN codes left.'.format(MAX_TAN_CODE_COUNT - len(user.tan_codes)))


def save_db():
    session.commit()

atexit.register(save_db)