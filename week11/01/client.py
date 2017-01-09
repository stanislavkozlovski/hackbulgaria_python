class Client():
    def __init__(self, _id, username, balance, message):
        self.__username = username
        self.__balance = balance
        self.__id = _id
        self.__message = message

    @property
    def username(self):
        return self.__username

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
