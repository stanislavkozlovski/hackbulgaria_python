from database.updater import update_user_balance
from database.creator import create_tan_codes as db_create_tan_codes
from database.deleter import delete_tan_code
from utils.tan_codes import send_tan_codes
from settings.constants import TAN_CODE_COUNT_PER_GENERATION as MAX_TAN_CODE_COUNT

class Client:
    def __init__(self, _id, username, email, balance, message, tan_codes=set()):
        self.__username = username
        self.__email = email
        self.__balance = balance
        self.__id = _id
        self.__message = message
        self.__tan_codes = tan_codes

    @property
    def username(self):
        return self.__username

    @property
    def email(self):
        return self.__email

    @property
    def balance(self):
        return self.__balance

    @property
    def id(self):
        return self.__id

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, new_message):
        self.__message = new_message

    def deposit_money(self, amount: float):
        self.__balance += amount
        update_user_balance(self.__id, self.__balance)

    def withdraw_money(self, amount: float):
        if self.__balance < amount:
            print('You cannot withdraw more money than you have!')
            return False
        self.__balance -= amount
        update_user_balance(self.__id, self.__balance)

        return True

    def consume_tan_code(self, tan_code):
        if tan_code not in self.__tan_codes:
            raise Exception("The user does not have that TAN code!")
        self.__tan_codes.remove(tan_code)
        delete_tan_code(tan_code)

    def is_valid_tan_code(self, tan_code):
        return tan_code in self.__tan_codes

    def generate_tan_codes(self):
        if len(self.__tan_codes) == 0:
            tan_codes, success = send_tan_codes(self.email)
            if not success:
                print('Something went wrong when creating your TAN codes.')
                return
            self.__tan_codes = tan_codes
            db_create_tan_codes(self.__id, tan_codes)
        else:
            print('You still have {} TAN codes left.'.format(MAX_TAN_CODE_COUNT - len(self.__tan_codes)))
