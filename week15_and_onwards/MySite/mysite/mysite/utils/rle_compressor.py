"""
Courtesy of https://github.com/gnemoug/compression-RLE
"""
from string import ascii_uppercase as alphabet
import re


class RunLength:
    """Helper container class for string encoding"""

    def __init__(self, char, length=1):
        self.char = char
        self.length = length

    def __str__(self):
        if self.length <= 0:
            return ''
        if self.length == 1:
            return self.char
        if self.length >= 2 and self.length < 12:
            return (self.char * 2) + ('%d' % (self.length - 2))
        else:  # self.length >= 12
            return (self.char * 2) + ('%d' % (9 % self.length)) \
                   + str(RunLength(self.char, self.length - 11))


def compress(plainText):
    """
    Compress a string using the following scheme:

    - The input is a string, and the output is a compressed string
    - A valid input consists of one or more upper case english letters A-Z.
    - Any run of two or more of the same character should be converted to two of
      that character plus a number indicating how many repeated runs were
      compressed.
    - Only one digit may be used at a time, so if the run is quite long,
      then you must use multiple character/number pairs
    - Examples:
            A --> A
            AA --> AA0
            AAA --> AA1
            AAAA --> AA2
            AAAAAAAAAAAA --> AA9A
            AAAAAAAAAAAAA --> AA9AA0
            AAACBBC --> AA1CBB0C

    This method will raise a ValueError if called with an invalid input string.
    """

    compressedRuns = []
    current = RunLength('', 0)
    for char in plainText:
        if char not in alphabet:
            raise ValueError('Invalid input: ' \
                             + 'String includes non-capitalized or non-ASCII characters')
        if char == current.char:
            current.length += 1
        else:
            compressedRuns.append(str(current))
            current = RunLength(char)
    compressedRuns.append(str(current))  # Append the last run
    return ''.join(compressedRuns)


def decompress(compressedText):
    """
    Decode a string that was compressed using the same scheme as compress(string)
    Thus, the following will always be true:
    > originalInput == decompress(compress(originalInput))

    This method will raise a ValueError if called with an invalid input string
    parameter. To find out more about valid input strings, see compress().
    """

    decompressedRuns = []
    fmtRegex = re.compile(r'(\w)\1\d')
    continueOn = 0

    for index, char in enumerate(compressedText):
        if continueOn != 0:
            # We've already handled these characters. They're non-beginning
            # characters in a compressed substring (i.e. 'AA1'). Just skip them.
            continueOn -= 1
            continue

        if char not in alphabet:
            # Due to preceding conditional statement, this condition will only
            # be met when parsing an invalid input string. There will be no
            # issues with the digits in compressed substrings.
            raise ValueError('Invalid input: ' \
                             + 'String includes non-capitalized or non-ASCII characters')

        subStr = compressedText[index:index + 3]
        match = fmtRegex.match(subStr)

        if match:
            decompressedRuns.append(char * (int(subStr[2]) + 2))
            continueOn = 2
        else:
            decompressedRuns.append(char)
    return ''.join(decompressedRuns)