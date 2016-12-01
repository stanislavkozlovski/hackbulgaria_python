NEIGHBOURS_DIRECTION = [(0, -1), (0, 1), (1, 0), (-1, 0)]
TRAVERSED_STRAWBERRIES = set()  # holds tuples of the coordinates for each strawberry we've killed the neighbours of,
                                # so as not to waste time going through them again


def strawberries(rows, columns, days, dead_strawberries: list):
    global TRAVERSED_STRAWBERRIES
    TRAVERSED_STRAWBERRIES = set()  # reset our set

    if 0 > rows or rows > 10000 or 0 > columns or columns > 10000 or days < 0 or days > 1000:
        raise ValueError()  # invalid ipnut
    matrix = [[True] * columns for _ in range(rows)]  # build matrix, each alive strawberry is True
    # mark dead strawberries
    for row, col in dead_strawberries:
        matrix[row][col] = False

    # start going through the days
    for _ in range(days):
        dead_strawberries = day_pass(matrix, dead_strawberries)

    alive_strawberries = sum([sum(row) for row in matrix])  # get the count of all alive strawberries
    return alive_strawberries


def day_pass(matrix, dead_strawberries):
    """ A day passes and the strawberries die.
        Mark the dead strawberries in the matrix and return a list of the newly-deceased ones
        :return A list with the newly-dead strawberries, simply because there is no reason to return the old ones """
    recently_deceased_strawberries = []  # keep the newly-dead strawberries here
    for row, col in dead_strawberries:
        # try to kill the neighbouring strawberries
        if (row, col) not in TRAVERSED_STRAWBERRIES:
            for row_to_add, col_to_add in NEIGHBOURS_DIRECTION:
                new_row = row + row_to_add
                new_col = col + col_to_add
                if 0 <= new_row < len(matrix) and 0 <= new_col < len(matrix[new_row]):  # if it's in bounds
                    matrix[new_row][new_col] =  False
                    recently_deceased_strawberries.append((new_row, new_col))
        TRAVERSED_STRAWBERRIES.add((row, col))
    return recently_deceased_strawberries


#print(strawberries(8, 10, 2, [(4, 8), (2, 7)]))