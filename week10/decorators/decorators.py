import maya
import timeit
from time import sleep
from functools import wraps

"""
Make a decorator accepts that takes as many arguments as the function takes.
That decorator specify the types of the arguments that your function takes.
If any of the arguments does not match the type in the decorator raise a TypeError
"""


def accepts(*expected_types):
    def _accepts(func):
        def func_wrapper(*input_args):
            if len(expected_types) != len(input_args):
                raise TypeError("The decorator must take exactly as many arguments as the function")
            for idx, expected_type in enumerate(expected_types):
                if not isinstance(input_args[idx], expected_types[idx]):
                    raise TypeError("Argument {} of {function_name} is not {wanted_type}!".format(
                        idx, function_name=func.__name__, wanted_type=expected_types[idx].__name__
                    ))
            func(*input_args)
        return func_wrapper
    return _accepts


@accepts(str, int)
def say_hello(name, age):
    return "Hello, I am {}".format(name)
#
say_hello('da', 3)

"""
Make a decorator encrypt that takes an integer.
The decorator should encrypts the returned string of a function using the Caesar Cipher.
That integer is the encryptions key.
"""
letter_to_num = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", range(26)))
num_to_letter = {val: key for key, val in letter_to_num.items()}  # turned around


def caesar_cipher(text, key):
    upper_plaintext = text.upper()
    # encipher
    cipher_text = ''
    for c in upper_plaintext:
        if c.isalpha():
            cipher_text += num_to_letter[(letter_to_num[c] + key) % 26]  # get the position after adding the key
        else:
            cipher_text += c  # if it's not a letter, don't change it

    return cipher_text


def encrypt(*args):
    key = args[0]
    def _encipher(func):
        @wraps(func)
        def func_wrapper(*args):
            plaintext = func(*args)
            return caesar_cipher(plaintext, key)
        return func_wrapper
    return _encipher


@encrypt(2)
def get_low():
    return "Get get get low"


print(get_low())


"""
Make a decorator log that takes a file_name and writes in to this file a log. New line for every call of the decorated function.
"""


def log(*args):
    filename = args[0]
    def _log(func):
        def func_wrapper():
            with open(filename, 'a') as f:
                f.write('{func_name} was called at {date}\n'.format(
                    func_name=func.__name__,
                    date=maya.now().datetime()
                ))
        return func_wrapper
    return _log


@log('log.txt')
@encrypt(2)
def get_lower():
    return "Get get get, get low"

get_lower()


"""
Make a decorator performance that takes an file_name and writes in to this file a log.
New line for every call of the decorated function.
This decorator should log the time needed for the decorated function to execute.
"""


def performance(*args):
    file_name = args[0]
    def _performance(func):
        def func_wrapper():
            start = timeit.default_timer()
            func()
            end = timeit.default_timer()
            with open(file_name, 'a') as f:
                f.write("{func_name} was called and took {elapsed_time:.2f} seconds to complete\n".format(
                    func_name=func.__name__,
                    elapsed_time=end-start
                ))
        return func_wrapper
    return _performance


@performance('performance-log.txt')
def sleep_lower():
    sleep(2)
    return "I am done!"

sleep_lower()

