"""
Implement a Python script, called cat2.py that takes multiple arguments - file names and prints the contents of all files to the console, in the order of the arguments.

The number of the files that are given as arguments is unknown.

There should be a newline between every two files that are printed.

Boilerplate

# cat2.py
import sys


def main():
    pass

if __name__ == '__main__':
    main()
Examples

If we have two files - file1.txt and file2.txt in the same directory with cat2.py and:


"""
import sys
import os


def main():
    if len(sys.argv) < 2:
        print("Please enter at least one argument, the file you want to see the contents of.")
        print("ex: python3 cat.py file.txt")
        exit()

    for file_name in sys.argv[1:]:
        if not os.path.exists(file_name):
            print("{} does not exist!".format(file_name))
            continue
        print(file_name)
        print('-'*40)
        with open(file_name, 'r') as f:
            contents = f.read()
            print(contents)
        print('-'*40)
        print()


if __name__ == '__main__':
    main()