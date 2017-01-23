import sys

class Field:
    def save_value(self, value):
        self.value = self.validate(value)
    pass


class PrimaryKey(Field):
    def __str__(self):
        return 'INTEGER PRIMARY KEY AUTOINCREMENT'


class IntegerColumn(Field):
    def __init__(self, max_integer: int=sys.maxsize):
        self.max_integer = max_integer

    def __str__(self, creation: bool=False):
        return 'INTEGER'

    def validate(self, value):
        if not isinstance(value, int):
            raise Exception('An IntegerColumn must hold an integer!')
        if value > self.max_integer:
            raise Exception(f'The maximum integer value for this columns is {self.max_integer}')

        return value


class TextColumn(Field):
    def __init__(self, max_len: int=sys.maxsize):
        self.max_len = max_len
    def __str__(self):
        return 'TEXT'

    def validate(self, value):
        if not isinstance(value, str):
            raise Exception('A TextColumn must hold a string!')
        if len(value) > self.max_len:
            raise Exception(f'This TextColumn does not support Text longer than {self.max_len} characters!')
        return value
