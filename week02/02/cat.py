"""
Implement the cat command - Print file contents

In Linux, there is a very useful command, called cat:

$ cat file.txt
This is some file
And cat is printing it's contents
Implement a Python script, called cat.py that takes one argument - a filename and prints the contents of that file to the console.

Boilerplate

# cat.py
import sys


def main():
    pass

if __name__ == '__main__':
    main()
"""
import sys
import os


def main():
    if len(sys.argv) != 2:
        print("Please enter one argument, the file you want to see the contents of.")
        print("ex: python3 cat.py file.txt")
        exit()

    file_name = sys.argv[1]

    if not os.path.exists(file_name):
        print("{} does not exist!".format(file_name))
        exit()

    with open(file_name, 'r') as f:
        contents = f.read()
        print(contents)


if __name__ == '__main__':
    main()