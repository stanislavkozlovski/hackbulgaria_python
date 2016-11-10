# one matrix implementation


def build_matrix():
    input_count = int(input())
    matrix = []
    max_col = 0
    # build the matrix
    for _ in range(input_count):
        row, col = tuple(map(lambda x: int(x), input().split()))
        # check out of bounds for rowand handle it
        while row >= len(matrix):
            matrix.append([])
        # check out of bounds for col and handle it
        while col >= len(matrix[row]):
            matrix[row].append(False)

        matrix[row][col] = True

        if col > max_col:
            max_col = col

    # depending on the input, we migt have some existing rows that have not been addressed at all
    # ex: input: 2 1, row 1 will simply exist as an empty list but nothing more
    # so, we fill up the empty values to create an even matrix
    # fill up the rest of the matrix with false values
    for row in matrix:
        while max_col >= len(row):
            row.append(False)

    return matrix


def game_turn(matrix):
    # iterate the matrix and keep a list of cells that should be revived or killed
    cells_to_revive, cells_to_die = get_cells_to_die_and_revive()

    update_matrix(matrix, cells_to_revive, cells_to_die)


def get_cells_to_die_and_revive():
    # iterate through the matrix and knowing the rules, return a list of cells that need to be revived and that need to die
    cells_to_revive = []
    cells_to_die = []

    for row_idx, row in enumerate(matrix):
        for col_idx, col in enumerate(row):
            current_cell_state = col
            live_neighbours_count = get_live_neighbours_count(matrix, row_idx, col_idx)

            if current_cell_state:  # is alive
                if live_neighbours_count < 2: # fewer than two live neighbours - dies
                    cells_to_die.append((row_idx, col_idx))
                elif live_neighbours_count > 3:  # more than three live neighbours - dies by overpopulation
                    cells_to_die.append((row_idx, col_idx))
                # else: lives on
            else:  # dead cell
                if live_neighbours_count == 3:
                    cells_to_revive.append((row_idx, col_idx))

    return cells_to_revive, cells_to_die


def update_matrix(matrix, cells_to_revive, cells_to_die):
    # change matrix
    for x, y in cells_to_revive:
        matrix[x][y] = True
    for x, y in cells_to_die:
        matrix[x][y] = False
    print_matrix(matrix)


def get_live_neighbours_count(matrix: list, x: int, y: int):
    return len([matrix[x2][y2] for x2 in range(x - 1, x + 2)
                for y2 in range(y - 1, y + 2)
                if ((0 <= x2 < len(matrix))  # not out of bounds
                    and (x != x2 or y != y2)  # not the same node
                    and (0 <= y2 < len(matrix[x])))  # not out of bounds
                    and matrix[x2][y2]])  # it's true


def print_matrix(matrix):
    for row in matrix:
        row_str = ''
        for char in row:
            if char:
                row_str += 'X'
            else:
                row_str += '-'
        print(row_str)


def main():
    matrix = build_matrix()
    while True:
        game_turn(matrix)
        input('Enter any key to see another turn of the game!')


if __name__ == '__main__':
    main()