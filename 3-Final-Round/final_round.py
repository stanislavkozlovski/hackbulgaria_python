"""
A number is called balanced, if we take the middle of it and the sums of the left and right parts are equal.

For example, the number 1238033 is balanced, because it's left part is 123 and right part is 033.

We have : 1 + 2 + 3 = 0 + 3 + 3 = 6.

A number with only one digit is always balanced!

Implement a function is_number_balanced(n) that checks if n is balanced.
"""


def is_number_balanced(n: int):
    number_str = str(n)
    numbers_len = len(number_str)

    if numbers_len == 1:
        return True
    else:
        # if the number's length is odd, we want to skip the mid index
        # so in 12321, we want to check if 12 is equal to 21 (we skip 3)
        # in 1221, we want to check if 12 is equal to 21 again
        skip_mid_index = 1 if numbers_len % 2 != 0 else 0
        mid_index = numbers_len // 2

        left_part = number_str[0:mid_index]
        right_part = number_str[mid_index + skip_mid_index:]

        return sum(int(digit) for digit in left_part) == sum(int(digit) for digit in right_part)

print('-'*20)
print("IS NUMBER BALANCED?")
print('-'*20)

print(is_number_balanced(9))
# True
print(is_number_balanced(4518))
# True
print(is_number_balanced(28471))
# False
print(is_number_balanced(1238033))
# True


"""
Implement a function, called `increasing_or_decreasing(seq)` where `seq` is a `list` of integers.

The function should return `Up!`, if the given sequence is monotonously increasing.
If monotonously decreasing return `Down!` .
If both of the condintions are not satisfied, then return `False`.

And before you skip this problem, because of the math terminology, let me explain:

**A sequence is monotonously increasing if for every two elements `a` and `b`, that are next to each other (`a` is before `b`), we have `a` < `b`.**

For example, `[1,2,3,4,5]` is monotonously increasing, but `[1,2,3,4,5,1]` is not.
"""

def increasing_or_decreasing(seq: list):
    """ returns whether or not the list is monotonously increasing/decreasing """
    rest_seq = seq[1:]

    """ what we do is we create another list, that's one item behind the original sequence.
        then, when we compare the original seq[0] to rest_seq[0], we're essentially comparing
        seq[0] to seq[1], because rest_seq is always 1 ahead"""
    # is increasing
    isIncreasing = all([rest_seq[idx] > seq[idx] for idx, el in enumerate(rest_seq)])
    # is decreasing
    isDecreasing = all([rest_seq[idx] < seq[idx] for idx, el in enumerate(rest_seq)])

    if isIncreasing:
        return "Up!"
    elif isDecreasing:
        return "Down!"
    else:
        return False


print('-'*20)
print("INCREASING OR DECREASING")
print('-'*20)

print(increasing_or_decreasing([1,2,3,4,5]))
# Up!
print(increasing_or_decreasing([5,6,-10]))
# False
print(increasing_or_decreasing([1,1,1,1]))
# False
print(increasing_or_decreasing([9,8,7,6]))
# Down!


"""
Implement a function get_largest_palindrome(n), which return the largest palindrome smaller than n. Given number n can also be palindrome.
"""


def get_largest_palindrome(n: int):
    while n > 0:
        n -= 1
        if str(n) == str(n)[::-1]:
            return str(n)
    return "No largest palindrome available!"

print('-'*20)
print("GET LARGEST PALINDROME")
print('-'*20)

print(get_largest_palindrome(99))
# 88
print(get_largest_palindrome(252))
# 242
print(get_largest_palindrome(994687))
# 994499
print(get_largest_palindrome(754649))
# 754457

"""
You are given a string, where there can be numbers. Return the sum of all numbers in that string (not digits, numbers)
"""


def sum_of_numbers(input: str):
    import re
    numbers_in_str = re.findall(r'\d+', input)
    return sum(int(num) for num in numbers_in_str)

print('-'*20)
print("SUM OF NUMBERS")
print('-'*20)

print(sum_of_numbers("ab125cd3"))
# 128
print(sum_of_numbers("ab12"))
# 12
print(sum_of_numbers("ab"))
# 0

"""
Implement a function birthday_ranges(birthdays, ranges) We have a list birthdays and list of tuples ranges. birthdays - range from 0 to 365, ranges - ranges (one range is a tuple of two numbers - start and end0.

We want to calculate, for each tuple, how many people are born in that range (between start and end inclusive).

For example:

Birthdays - [5, 10, 6, 7, 3, 4, 5, 11, 21, 300, 15]
Ranges - [(4, 9), (6, 7), (200, 225), (300, 365)]
Will give the result:

[5, 2, 0, 1]
As we can see, betweeh 4 and 9, inclusive, there are 5 people with birthdays - 5, 6, 7, 4, 5.Between 300 and 365 there is exatly one birthday - 300.
"""

def birthday_ranges(birthdays: list, ranges: list):
    """

    :param birthdays: list of all the birthdays
    :param ranges: list of tuples, containing ranges (4,9) for ex
    :return: for each tuple in ranges, the amount of birthdays in birthdays
    """
    people_in_range = []
    # iterate through ranges
    for range_start, range_end in ranges:
        # get the birthdays that are in the range
        people_in_range.append(len([birthday for birthday in birthdays if range_start <= birthday <= range_end]))

    return people_in_range


print('-'*20)
print("BIRTHDAY RANGES")
print('-'*20)

print(birthday_ranges([1, 2, 3, 4, 5], [(1, 2), (1, 3), (1, 4), (1, 5), (4, 6)]))
# [2, 3, 4, 5, 2]

"""
Before the smartphones, when you had to write some message, the keypads looked like that:

Nokia 3310 Keypad

For example, on such keypad, if you want to write Ruby, you had to press the following sequence of numbers:

7778822999
Each key contains some letters from the alphabet. And by pressing that key, you rotate the letters until you get to your desired one.

It's time to implement some encode / decode functions for the old keypads!

numbers_to_message(pressed_sequence)

First, implement the function that takes a list of integers - the sequence of numbers that have been pressed. The function should return the corresponding string of the message.

There are a few special rules:

If you press 1, the next letter is going to be capitalized
If you press 0, this will insert a single white-space
If you press a number and wait for a few seconds, the special breaking number -1 enters the sequence. This is the way to write different letters from only one keypad!
Few examples:

numbers_to_message([2, -1, 2, 2, -1, 2, 2, 2]) = "abc"
numbers_to_message([2, 2, 2, 2]) = "a"
numbers_to_message([1, 4, 4, 4, 8, 8, 8, 6, 6, 6, 0, 3, 3, 0, 1, 7, 7, 7, 7, 7, 2, 6, 6, 3, 2])
=
"Ivo e Panda"
message_to_numbers(messsage)

This function takes a string - the message and returns the minimal keystrokes that you need to write that message

Few examples:

message_to_numbers("abc") = [2, -1, 2, 2, -1, 2, 2, 2]
message_to_numbers("a") = [2]
message_to_numbers("Ivo e Panda")
=
[1, 4, 4, 4, 8, 8, 8, 6, 6, 6, 0, 3, 3, 0, 1, 7, 2, 6, 6, 3, 2]
message_to_numbers("aabbcc") = [2, -1, 2, -1, 2, 2, -1, 2, 2, -1, 2, 2, 2, -1, 2, 2, 2]
"""

def group(arr: list):
    master_group = []
    last_num = arr[0]
    curr_group = []  # the group of consecutive numbers
    for num in arr:
        if num != last_num:  # if  the consecutive streak has ended, add the streak to the master group and start counting
            master_group.append(curr_group)  # add the group
            curr_group = []  # reset the current group

        curr_group.append(num)
        last_num = num

    master_group.append(curr_group)  # add the last group
    return master_group

CAPITAL_LETTER_KEY = 1
BREAK_KEY = -1
SPACE_KEY = 0

key_combinations_to_letters = {
    2: ['a', 'b', 'c'],
    3: ['d', 'e', 'f'],
    4: ['g', 'h', 'i'],
    5: ['j', 'k', 'l'],
    6: ['m', 'n', 'o'],
    7: ['p', 'q', 'r', 's'],
    8: ['t', 'u', 'v'],
    9: ['w', 'x', 'y', 'z']
}

def numbers_to_message(pressed_sequence: list):
    # split the sequence into grouped elements, for which we're going to use the group functio we created last time
    groups = group(pressed_sequence)  # list of lists, [[1,1], [-1], [2]]
    message = ''
    capital = False  # indicates if the next number should be a capital
    for sequence in groups:
        if sequence[0] == SPACE_KEY:
            message += ' '
        elif sequence[0] == CAPITAL_LETTER_KEY:
            capital = True
        elif sequence[0] == BREAK_KEY:
            continue
        else:
            sequence_key = sequence[0]  # 2, for example

            # check if the key is repeated too many times and it needs to flip, like 22222 (5 times, meaning we will
            # essentially be entering 22. it goes past 222 and on to 22
            key_max_length = len(key_combinations_to_letters[sequence_key])
            desired_count = len(sequence) % key_max_length

            if desired_count == 0:
                # 2's max is 3(2222 is invalid). if we've entered 3, 3%3 it'll give 0, but we mean 222.
                #  Same with 6%3, it'll return 0, but we mean 222
                desired_count = key_max_length

            sequence = [sequence_key] * desired_count
            letter = key_combinations_to_letters[sequence_key][len(sequence) - 1]

            if capital:
                letter = letter.upper()
                capital = False

            message += letter

    return message

print('-'*20)
print('NUMBERS TO MESSAGES')
print('-'*20)
print(numbers_to_message([2, -1, 2, 2, -1, 2, 2, 2]))
print(numbers_to_message([2, 2, 2, 2]))
print(numbers_to_message([1, 4, 4, 4, 8, 8, 8, 6, 6, 6, 0, 3, 3, 0, 1, 7, 7, 7, 7, 7, 2, 6, 6, 3, 2]))

"""
message_to_numbers(messsage)

This function takes a string - the message and returns the minimal keystrokes that you need to write that message
"""

letters_to_key_combinations = {letter: str(k)*(idx+1) for k, v in key_combinations_to_letters.items() for idx, letter in enumerate(v) }

def message_to_numbers(message: str):
    """ loop through the message and return it in keystrokes"""
    keystrokes = []
    for letter in message:
        if letter.isupper():
            # we want it to be a capital letter
            keystrokes.append(1)
        if letter == ' ':
            keystrokes.append(int(SPACE_KEY))
        else:
            sequence_str = letters_to_key_combinations[letter.lower()]
            seq_list = list(sequence_str)  # ['2', '2', '2']
            # convert seq list to integers
            seq_list = [int(digit) for digit in seq_list]  # [2, 2, 2]

            if keystrokes and keystrokes[-1] == seq_list[0]:
                # we have two consecutive numbers, meaning we want to break with -1
                keystrokes.append(-1)
            keystrokes.extend(seq_list)

    return keystrokes

print('-'*20)
print("MESSAGE TO NUMBERS")
print('-'*20)
print(message_to_numbers("abc"))
#[2, -1, 2, 2, -1, 2, 2, 2]
print(message_to_numbers("a"))
#[2]
print(message_to_numbers("Ivo e Panda"))
#[1, 4, 4, 4, 8, 8, 8, 6, 6, 6, 0, 3, 3, 0, 1, 7, 2, 6, 6, 3, 2]
print(message_to_numbers("aabbcc"))
#[2, -1, 2, -1, 2, 2, -1, 2, 2, -1, 2, 2, 2, -1, 2, 2, 2]



"""
Have you every wondered how many fridays are there in one year?

The count can be 52 or 53, depending on the weeks of that year (leap or not) and the start of the year.

If an year contains 53 fridays, we call that "A Friday Year"

You are to implement a function, called friday_years(start, end), where start and end are integers, representing years.

The function should return the count of all friday years between [start, end]
"""
# Now if the year starts on a Friday in a non-leap year, you end up with 53 Fridays.
#  Or if either of the first two days lands on a Friday during a leap year, then you can also get 53 Fridays.
#  Check the calendars below for January and December of 2016 to see exactly where the year starts and ends.

import calendar
import datetime


def friday_years(start_year: int, end_year: int):
    friday_years_ = 0
    for year in range(start_year, end_year+1):
        if calendar.isleap(year):
            first_day = datetime.datetime(year, 1, 1)  # type: datetime
            second_day = datetime.datetime(year, 1, 2)  # type: datetime
            if first_day.weekday() == 5 or second_day.weekday() == 5:
                friday_years_ += 1
        else:
            # non leap year
            # January 1st, Year
            day = datetime.datetime(year, 1, 1)  # type: datetime
            if day.weekday() == 5:
                # january 1st is friday
                # meaning we have 53 fridays this year
                friday_years_ += 1


    return friday_years_

print(friday_years(1000, 2000))
# 178
print(friday_years(1753, 2000))
# 44
print(friday_years(1990, 2015))
# 4