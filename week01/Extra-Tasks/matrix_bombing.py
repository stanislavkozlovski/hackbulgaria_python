"""
Matrix Bombing

You are givn a NxM matrix of integer numbers.

We can drop a bomb at any place in the matrix, which has the following effect:

All of the 3 to 8 neighbours (depending on where you hit!) of the target are reduced by the value of the target.
Numbers can be reduced only to 0 - they cannot go to negative.
For example, if we have the following matrix:

10  10  10
10   9  10
10  10  10
and we drop bomb at 9, this will result in the following matrix:

1 1 1
1 9 1
1 1 1
Implement a function called matrix_bombing_plan(m).

The function should return a dictionary where keys are positions in the matrix, represented as tuples, and values are the total sum of the elements of the matrix, after the bombing at that position.

The positions are the standard indexes, starting from (0, 0)

For example if we have the following matrix:

1 2 3
4 5 6
7 8 9
and run the function, we will have:

{(0, 0): 42,
 (0, 1): 36,
 (0, 2): 37,
 (1, 0): 30,
 (1, 1): 15,
 (1, 2): 23,
 (2, 0): 29,
 (2, 1): 15,
 (2, 2): 26}
We can see that if we drop the bomb at (1, 1) or (2, 1), we will do the most damage!
"""
from pprint import pprint


def main():
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]

    sums_after_bombing = matrix_bombing_plan(matrix)
    pprint(sums_after_bombing)


def matrix_bombing_plan(m: list):
    matrix_sum = get_matrix_sum(m)  # hold the sum of the original matrix
    # neighbour will hold the neighbours of each Key: Tuple, Value: List of Tuples (the neighbour of the key)
    neighbours = fill_neighbours(m)  # type: dict
    # result will hold positions in the matrix and it's sum after the bombing at those coordinates
    result = {}

    for row in range(len(m)):
        for col in range(len(m[row])):
            damage_done = bomb_matrix(m, row, col, neighbours)
            # the new sum will be the damage done subtracted from the original matrix sum
            result[(row, col)] = matrix_sum - damage_done

    return result


def get_matrix_sum(m: list):
    return sum(sum(row) for row in m)

def bomb_matrix(matrix: list, row, col, neighbours: dict) -> int:
    """ given the matrix and coordinates, bomb the matrix,
        then return the damage you've done"""
    value = matrix[row][col]
    damage = 0

    for neighbour_x, neighbour_y in neighbours[(row, col)]:
        neighbour_value = matrix[neighbour_x][neighbour_y]
        difference = neighbour_value - value
        # we cannot go under 0, so we add the damage accordingly
        if difference >= 0:
            damage += value
        else:
            damage += neighbour_value

    return damage


def fill_neighbours(matrix):
    # neighbour will hold the neighbours of each Key: Tuple, Value: List of Tuples (the neighbour of the key)
    neighbours = {}  # type: dict

    # fill neighbours
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            neighbours[(row, col)] = get_neighbours(matrix, row, col)

    return neighbours


def get_neighbours(matrix, row, col) -> list:
    neighbours = []

    # top neighbours
    if row-1 >= 0:
        for top_col in range(col-1, col+2):
            if top_col >= 0 and top_col < len(matrix[row-1]):
                neighbours.append((row-1, top_col))

    # left neighbour
    if col-1 >= 0:
        neighbours.append((row, col-1))
    # right neighbour
    if col+1 < len(matrix[row]):
        neighbours.append((row, col+1))

    # bot neighbours
    if row+1 < len(matrix):
        for bot_col in range(col-1, col+2):
            if bot_col >= 0 and bot_col < len(matrix[row+1]):
                neighbours.append((row+1, bot_col))

    return neighbours


if __name__ == "__main__":
    main()