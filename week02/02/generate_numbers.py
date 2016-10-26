"""
Implement a Python script, called generate_numbers.py that takes two arguments - a filename and an integer n.

The script should create a file with the filename and print n random integers, separated by " ".

For random integers, you can use:

from random import randint
print(randint(1, 1000))


$ python3.4 generate_numbers.py numbers.txt 100
$ cat numbers.txt
612 453 555 922 120 840 173 98 994 461 392 739 982 598 610 205 13 604 304 591 830 313 534 47 945 26 975 338
"""

import sys
from random import randint

MAX_RAND_INT = 1000


def main():
    if len(sys.argv) < 3:
        print("Please enter two arguments: the file name and the number of integers you want in it.")
        print("ex: python3 generate_numbers.py numbers.txt 100")

    file_name = sys.argv[1]
    # append .txt to the file name
    if file_name[-4:] != '.txt':
        file_name += '.txt'

    numbers_count = int(sys.argv[2])
    with open(file_name, 'a') as f:
        f.write(' '.join([str(randint(0, MAX_RAND_INT)) for _ in range(numbers_count)]))

if __name__ == '__main__':
    main()