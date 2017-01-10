from database.updater import update_user_balance

class Client:
    def __init__(self, _id, username, email, balance, message):
        self.__username = username
        self.__email = email
        self.__balance = balance
        self.__id = _id
        self.__message = message

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
