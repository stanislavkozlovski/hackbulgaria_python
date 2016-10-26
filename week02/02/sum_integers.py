"""
Implement a Python script, called sum_numbers.py that takes one argument - a filename which has integers, separated by " ".

The script should print the sum of all integers in that file.


If we use the generated file from Problem 3:

$ python3.4 sum_numbers.py numbers.txt
47372
"""
import sys


def main():
    if len(sys.argv) != 2:
        print("Please enter one argument, the name of a text file with numbers in it.")

    file_name = sys.argv[1]
    with open(file_name, 'r', encoding='UTF-8') as f:
        contents = f.readline()
        print(sum([int(digit) for digit in contents.split()]))

if __name__ == '__main__':
    main()