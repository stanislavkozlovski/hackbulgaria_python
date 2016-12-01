NEIGHBOURS_DIRECTION = [(0, -1), (0, 1), (1, 0), (-1, 0)]
DONE_NEIGHBOURS = set()

def strawberries(rows, columns, days, dead_strawberries: list):
    if 0 > rows or rows > 10000 or 0 > columns or columns > 10000 or days < 0 or days > 1000:
        raise ValueError()
    # build matrix
    matrix = [[True] * columns for _ in range(rows)]
    # mark dead strawberries
    for row, col in dead_strawberries:
        matrix[row][col] = False
    for _ in range(days):
        dead_strawberries = day_pass(matrix, dead_strawberries)
    alive_strawberries = sum([sum(row) for row in matrix])
    return alive_strawberries


def day_pass(matrix, dead_strawberries):
    """ A day passes and the strawberries die.
        Mark the dead strawberries in the matrix and return a list of the newly-deceased ones
        :return A list with the newly-dead strawberries, simply because there is no reason to return the old ones """
    recently_deceased_strawberries = []  # keep the newly-dead strawberries here
    for row, col in dead_strawberries:
        # go through the neighbours
        if (row, col) not in DONE_NEIGHBOURS:
            for row_to_add, col_to_add in NEIGHBOURS_DIRECTION:
                new_row = row + row_to_add
                new_col = col + col_to_add
                if 0 <= new_row < len(matrix) and 0 <= new_col < len(matrix[new_row]):  # if it's in bounds
                    matrix[new_row][new_col] =  False
                    recently_deceased_strawberries.append((new_row, new_col))
        DONE_NEIGHBOURS.add((row, col))
    return recently_deceased_strawberries



print(strawberries(400, 803, 99, [(399, 200), (196, 202)]))