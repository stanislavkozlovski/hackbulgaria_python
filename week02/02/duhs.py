"""
In linux, if we want to know the size of a directory, we use the du command. For example:

$ du -hs /home/radorado/code
2,3G  /home/radorado/code
-h flag is for "human readable" which means we get the size in gigabytes, not bytes.
-s flag is for silent. We don't want to print every file that we go through.
In a file called duhs.py, implement the logic of du -hs /some/path, where /some/path is obtained as an argument to the file.

Example usage:

$ python3.4 duhs.py /home/slavyana/code
/home/slavyana/code size is: 2.3G
THIS IS NOT THE SOLUTION WE WANT:

from subprocess import call
import sys

path = sys.argv[1]

call(["du", "-s", "-h", path])
Hints

Check the os python module.
Many of the methods raise errors. In order to deal with an error you can do the following things:
try:
    os.something(path)
except FileNotFoundError as error:
    print(error)
When you except the error, it wont crash your program.
"""
import os, sys
BYTES_IN_A_GIGABYTE = 1000000000
BYTES_IN_A_KILOBYTE = 1000


def main():
    file_path, silent_flag, human_readable_flag = read_commands()

    total_size = recurse_dir_and_get_size(file_path, silent_flag, human_readable_flag)

    if human_readable_flag:
        # convert to GB and string
        total_size /= BYTES_IN_A_GIGABYTE
        total_size = str(total_size) + 'G'

    print("{path}'s size is {size}".format(path=file_path, size=total_size))


def recurse_dir_and_get_size(dir_path: str, silent_flag: bool, human_readable_flag: bool) -> int:
    total_size = 0

    for filename in os.listdir(dir_path):
        if os.path.isdir(filename):
            recurse_dir_and_get_size(dir_path, silent_flag, human_readable_flag)
        else:
            full_path = os.path.join(dir_path, filename)
            file_size = os.path.getsize(full_path)
            total_size += file_size
            if not silent_flag:
                if human_readable_flag:
                    # convert to KBs and string
                    file_size /= BYTES_IN_A_KILOBYTE
                    file_size = str(file_size) + ' KB'

                print("{size}\t\t{name}".format(size=file_size, name=filename))

    return total_size


def read_commands() -> tuple:
    """
    read the parameters from the commandline
    returns the file path and both allowed flags
    """
    silent_flag = False
    human_readable_flag = False
    file_path = sys.argv[1]
    if len(sys.argv) > 2:
        flags = sys.argv[1]
        file_path = sys.argv[2]
        if 's' in flags:
            silent_flag = True
        if 'h' in flags:
            human_readable_flag = True

    return file_path, silent_flag, human_readable_flag

if __name__ == '__main__':
    main()