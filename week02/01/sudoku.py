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

def sudoku_solved(sudoku_matrix: list) -> bool:
    # check rows
    print(check_rows(sudoku_matrix))
    print(check_cols(sudoku_matrix))
    print(check_boxes(sudoku_matrix))

def check_boxes(sudoku_matrix: list) -> bool:
    """ returns whether the sudoku's boxes are valid"""
    start_index = 0
    end_index = 3
    col_start_index = 0
    col_end_index = 3

    for i in range(len(sudoku_matrix)):
        box = []

        for row in sudoku_matrix[start_index:end_index]:
            box.extend(row[col_start_index:col_end_index])

        col_start_index += 3
        col_end_index += 3

        if col_end_index > len(sudoku_matrix):
            col_start_index = 0
            col_end_index = 3
            start_index += 3
            end_index += 3
        
        if set(box) != {1,2,3,4,5,6,7,8,9}:
            return False

    return True

def check_rows(sudoku_matrix:list) -> bool:
    for row in sudoku_matrix:
        if set(row) != {1,2,3,4,5,6,7,8,9}:
            return False

    return True



def rotate_matrix(m: list):
    """
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            ret[i, j] = matrix[n - j - 1, i];
        }
    }
    """
    from copy import deepcopy
    rotated_matrix = deepcopy(m)

    for row in range(len(m)):
        for col in range(len(m[row])):
            rotated_matrix[row][col] = m[len(m) - col - 1][row]

    return rotated_matrix

def check_cols(sudoku_matrix:list) -> bool:
    """ check if the columns are valid solved sudoku"""
    # 1.Rotate the matrix to get all the columns as rows
    # 2. Check the new rows (in reality, the cols)
    rotated_matrix = rotate_matrix(sudoku_matrix)
    return check_rows(rotated_matrix)


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