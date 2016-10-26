"""
You are given a rectangular table filled with characters and a word. Your task is to count the occurences of a word in the table. The word can be found horizontaly, vertically and across both left to right and right to left.

For example:

Find the word ivan in the table:

i	v	a	n
e	v	n	h
i	n	a	v
m	v	v	n
q	r	i	t
Result:

3
The first thing you need to do is to input the word you are looking for. You need to provide the number of rows and columns of your table. Then input the characters into the table.

Note: If the word you are looking for is longer than the length of your rows, columns or diagonals, you need to return message to the user that the input was invalid.
"""

def main():
    # read the input
    word = input()
    rows, cols = [int(x) for x in input().split()]
    matrix = []
    for _ in range(rows):
        # read the rows and parse them
        row = input().split()
        if len(row) < cols:
            print("Invalid number of rows or columns!")
            exit()
        matrix.append(row)

    # iterate through the matrix and check for the word
    occurences = 0
    for row in range(rows):
        for col in range(cols):
            if matrix[row][col] == word[0]:
                # if we start with the same letter, start trying to find it
                if check_horizontal(matrix, row, col, word):
                    occurences += 1
                #if check_horizontal(matrix, row, col, word, backwards=True):
                 #   occurences += 1
                if check_vertical(matrix, row, col, word):
                    occurences += 1
               # if check_vertical(matrix, row, col, word, backwards=True):
                #    occurences += 1
                if check_diagonal(matrix, row, col, word):
                    occurences += 1
                if check_diagonal(matrix, row, col, word, backwards=True):
                    occurences += 1

    print(occurences)


def check_horizontal(matrix: list, row, start_col, word: str, backwards: bool=False):
    """
    :param backwards: bool indicating if we want to check backwards or forwards
    """
    built_word = ""
    direction_max_col = len(matrix[row]) if not backwards else -1
    increment = 1 if not backwards else -1
    for col in range(start_col, direction_max_col, increment):
        built_word += matrix[row][col]

        if built_word == word:
            return True

    return False


def check_vertical(matrix: list, start_row, col, word: str, backwards: bool=False):
    built_word = ""
    direction_max_row = len(matrix) if not backwards else -1
    increment = 1 if not backwards else -1
    for row in range(start_row, direction_max_row, increment):
        built_word += matrix[row][col]

        if built_word == word:
            return True

    return False


def check_diagonal(matrix: list, row, col, word: str, backwards: bool=False):
    built_word = ""
    increment = 1 if not backwards else -1

    while True:
        if row >= len(matrix) or col >= len(matrix[row]) or row < 0 or col < 0:
            break  # out of bounds

        built_word += matrix[row][col]

        if built_word == word:
            return True
        row += increment
        col += increment

    return False

if __name__ == "__main__":
    main()