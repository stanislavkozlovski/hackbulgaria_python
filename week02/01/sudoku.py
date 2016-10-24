"""
Implement a function, called sudoku_solved(sudoku), that checks if the given sudoku matrix is solved correctly.

sudoku is a 9x9 matrix of integers.

A sudoku is solved correctly, if:

Each row contains the numbers from 1 do 9 without repeating a number
Each column contains the numbers from 1 to 9, without repeating a number
All 3x3 subgrids contains the numbers from 1 to 9, without repeating a number
For better reference, check Wikipedia - http://en.wikipedia.org/wiki/Sudoku

Signature

def sudoku_solved(sudoku):
    # Implementation
Test examples

sudoku_solved([
[4, 5, 2, 3, 8, 9, 7, 1, 6],
[3, 8, 7, 4, 6, 1, 2, 9, 5],
[6, 1, 9, 2, 5, 7, 3, 4 ,8],
[9, 3, 5, 1, 2, 6, 8, 7, 4],
[7, 6, 4, 9, 3, 8, 5, 2, 1],
[1, 2, 8, 5, 7, 4, 6, 3, 9],
[5, 7, 1, 8, 9, 2, 4, 6, 3],
[8, 9, 6, 7, 4, 3, 1, 5 ,2],
[2, 4, 3, 6, 1, 5, 9, 8, 7]
])
True
sudoku_solved([
[1, 2, 3, 4, 5, 6, 7, 8, 9],
[1, 2, 3, 4, 5, 6, 7, 8, 9],
[1, 2, 3, 4, 5, 6, 7, 8, 9],
[1, 2, 3, 4, 5, 6, 7, 8, 9],
[1, 2, 3, 4, 5, 6, 7, 8, 9],
[1, 2, 3, 4, 5, 6, 7, 8, 9],
[1, 2, 3, 4, 5, 6, 7, 8, 9],
[1, 2, 3, 4, 5, 6, 7, 8, 9],
[1, 2, 3, 4, 5, 6, 7, 8, 9]
])
False

"""
from copy import deepcopy

VALID_SUDOKU_SET = {1, 2, 3, 4, 5, 6, 7, 8, 9}


def rotate_matrix(m: list):
    rotated_matrix = deepcopy(m)

    for row in range(len(m)):
        for col in range(len(m[row])):
            rotated_matrix[row][col] = m[len(m) - col - 1][row]

    return rotated_matrix


def sudoku_solved(sudoku_matrix: list) -> bool:
    return check_rows(sudoku_matrix) and check_cols(sudoku_matrix) and check_boxes(sudoku_matrix)


def check_boxes(sudoku_matrix: list) -> bool:
    """ returns whether the sudoku's boxes are valid"""
    start_index = 0
    end_index = 3
    col_start_index = 0
    col_end_index = 3

    while end_index < len(sudoku_matrix):
        """
        iterate through the matrix, taking 3 rows each time and taking 3 elements of each row to form a sudoku box
        we start at rows 0-3 (0,1,2) and take the first three elements of each for (col_start_index to col_end_index)
        after that, we increment the col indexes by 3 and take the second three elements of each row to form the
        second box. iterate again for the third and etc. Once we run out of boxes on the current rows,
        we go down to the next 3 rows
        """
        # list of all the elements in the box ex: [4, 1, 3, 2, 9, 6, 7, 5, 8]
        box = sum([row[col_start_index:col_end_index] for row in sudoku_matrix[start_index:end_index]], [])

        col_start_index += 3
        col_end_index += 3

        if col_end_index > len(sudoku_matrix):
            col_start_index = 0
            col_end_index = 3
            # increment row indexes
            start_index += 3
            end_index += 3
        
        if set(box) != VALID_SUDOKU_SET:
            return False

    return True


def check_rows(sudoku_matrix:list) -> bool:
    for row in sudoku_matrix:
        if set(row) != VALID_SUDOKU_SET:
            return False

    return True


def check_cols(sudoku_matrix:list) -> bool:
    """ check if the columns are valid solved sudoku"""
    # 1. Rotate the matrix to get all the columns as rows
    # 2. Check the new rows (in reality, the cols)
    rotated_matrix = rotate_matrix(sudoku_matrix)
    return check_rows(rotated_matrix)


print(sudoku_solved([
[4, 5, 2, 3, 8, 9, 7, 1, 6],
[3, 8, 7, 4, 6, 1, 2, 9, 5],
[6, 1, 9, 2, 5, 7, 3, 4 ,8],
[9, 3, 5, 1, 2, 6, 8, 7, 4],
[7, 6, 4, 9, 3, 8, 5, 2, 1],
[1, 2, 8, 5, 7, 4, 6, 3, 9],
[5, 7, 1, 8, 9, 2, 4, 6, 3],
[8, 9, 6, 7, 4, 3, 1, 5 ,2],
[2, 4, 3, 6, 1, 5, 9, 8, 7]
]))
# True

print(sudoku_solved([
[1, 2, 3, 4, 5, 6, 7, 8, 9],
[1, 2, 3, 4, 5, 6, 7, 8, 9],
[1, 2, 3, 4, 5, 6, 7, 8, 9],
[1, 2, 3, 4, 5, 6, 7, 8, 9],
[1, 2, 3, 4, 5, 6, 7, 8, 9],
[1, 2, 3, 4, 5, 6, 7, 8, 9],
[1, 2, 3, 4, 5, 6, 7, 8, 9],
[1, 2, 3, 4, 5, 6, 7, 8, 9],
[1, 2, 3, 4, 5, 6, 7, 8, 9]
]))
# False
