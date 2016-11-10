from collections import Counter
from math import sqrt, factorial


# A function for counting the digits of a number
def sum_of_digits(number) -> int:
    return sum([int(dig) for dig in str(abs(number))])

print(sum_of_digits(-25))


# Create list with the digits of a number
def to_digits(number) -> list:
    return [int(x) for x in str(number)]
print(to_digits(123413))


# Create number from array
def to_number(digits):
    return int("".join(str(digit) for digit in digits))
print(to_number([1,2,3,0,2,3]))


# Count the vowels in a string
def count_vowels(string):
    vowels = Counter(string.lower())
    return sum([vowel_count for vowel, vowel_count in vowels.items() if vowel in "aeiouy"])
print(count_vowels("love the game"))


# Count the consonants in a string
def count_consonants(string):
    consonants = Counter(string.lower())
    return sum([consonant_count for consonant, consonant_count in consonants.items() if consonant in "bcdfghjklmnpqrstvwxz"])
print(count_consonants("love the game"))


# Check if a given number is prime
def prime_number(number):
    if number == 2: return True
    return any([number % num != 0 for num in range(2, int(sqrt(number)) + 1)])
print(prime_number(2))


# Sum of the factorials of the digits in the number
def fact_digits(n):
    return sum([factorial(int(dig)) for dig in list(str(n))])
print(fact_digits(999))


# fibonacci sequence
def fibonacci(number):
    fibonacci_numbers = [0, 1]
    for i in range(2, number+1):
        fibonacci_numbers.append(fibonacci_numbers[i-1] + fibonacci_numbers[i-2])

    return fibonacci_numbers[1:]
print(fibonacci(10))


def fib_number(number):
    if number == 1:
        return 1
    if number == 0:
        return 0

    return fib_number(number-1) + fib_number(number-2)  # inefficient!
print(fib_number(5))


# Check if a given string is palindrome
def palindrome(string):
    string = str(string)
    return string[::-1] == string

print(palindrome("yabadabadoo"))
print(palindrome("yaay"))
print(palindrome(123))


# Dictionary with all characters from a string
def char_histogram(string):
    return Counter(string)

print(char_histogram("dadada"))


def number_is_balanced(number):
    digits = list([int(digit) for digit in list(str(number))])
    for idx, _ in enumerate(digits):
        if sum(digits[:idx-1]) == sum(digits[idx:]):
            return True

    return False

print(number_is_balanced(121))


def unique_chars_in_string(string):
    return Counter(string).keys()


def sort_words(words: list):
    return sorted(words)

print(sort_words(["grey", "bblue", "blue"]))


def char_tuple_histogram(string):
    histogram = dict(Counter(string))
    for char, count in histogram.items():
        if count > 1:
            histogram[char] = (count,)

    return histogram

print(char_tuple_histogram("dad"))


def most_odd_number_seq(number: str):
    Counter()


def pair_sort_people(people):
    from itertools import groupby
    # holds the person and the id associated with him
    person_key_dict = {}  # ex: Key: "L", Value: 1
    person_id = 0

    # convert each value to a tuple, holding a key that identifies the person
    for idx, person in enumerate(people):
        if person not in person_key_dict.keys():
            person_key_dict[person] = person_id
            person_id += 1
        people[idx] = (person, person_key_dict[person])

    grouped_people = []
    for key, group in groupby(sorted(people), lambda x: x[1]):
        grouped_people.append(list(group))

    # sort the groups by their length
    grouped_people = sorted(grouped_people, key=lambda x: len(x))

    # 1.     Take a copy of the list with the most members. This will be the destination list.
    grouped_people = list(reversed(grouped_people))
    destination_list = grouped_people[0]

    for other_list in grouped_people[1:]:
        # 2. Then take the list with the next largest number.
        # 3. Divide the destination list length by the smaller length to give a fractional value of greater than one.
        index_to_go = len(destination_list) / len(other_list)
        float_counter = 0
        for other_v in other_list:
            # 4. For each item in the second list, maintain a float counter.
            # Add the value calculated in the previous step, and mathematically round it to the nearest integer
            #  (keep the original float counter intact).
            #  Insert it at this position in the destination list and increment the counter by 1 to account for it.
            # Repeat for all list members in the second list.
            float_counter += index_to_go
            index = int(round(float_counter))
            float_counter += 1

            destination_list.insert(index, other_v)
        #  Repeat steps 2-5 for all lists.

    print(destination_list)


pair_sort_people(["S", "S", "D", "D", "D", "O", "S", "L", "R", "L", "B", "X"])