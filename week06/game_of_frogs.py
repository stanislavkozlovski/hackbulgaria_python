FROG_DIRECTIONS = {'R': -1,
                   'F': 1}
def main():
    max = 2
    frogs = ['F'] * max + ['_'] + ['R'] * max
    expected_output = ['R'] * max + ['_'] + ['F'] * max
    print(line_up_frogs(frogs, max, expected_output))


def line_up_frogs(frogs, frog_count, expected_output: list):
    """
    Algorithm is:

    Step 1:
    Count from 1 to frog_count, Moving left frogs - 'F' on Odd numbers and
    moving right frogs - 'R' on Even numbers. Depending on the number from 1 to frog_count, move that many frogs

    Step 2:
    Move frog_count frogs every turn, again following the odd/even number pattern, until you reached the desired result
    """
    first_part(frogs, frog_count)
    second_part(frogs, frog_count, expected_output)

    return frogs


def first_part(frogs, frog_count):
    """Count from 1 to frog_count, Moving left frogs - 'F' on Odd numbers and
    moving right frogs - 'R' on Even numbers. Depending on the number from 1 to frog_count, move that many frogs"""
    for turn in range(1, frog_count + 1):
        if turn % 2 == 0:
            move_frog(frogs, frogs_to_move=turn, frog_to_move='R')
        else:
            move_frog(frogs, frogs_to_move=turn, frog_to_move='F')


def second_part(frogs, frog_count, expected_output: list):
    """
    Try to move frog_count number of frogs each turn, while tracking if we go out of bounds with our
    index, following the pattern - move 'F' frogs on odd numbers and move 'R' frogs on even.
    Stop when we get the expected output.
    """
    turn = frog_count + 1
    while True:
        if turn % 2 == 0:
            move_frog(frogs, frog_count, 'R')
        else:
            move_frog(frogs, frog_count, 'F')
        turn += 1
        if frogs == expected_output:
            return

def move_frog(frogs, frogs_to_move, frog_to_move: str):
    start_idx = 0 if frog_to_move == 'R' else len(frogs) - 1

    for _ in range(frogs_to_move):  # move FROGS_TO_MOVE count frogs
        frog_idx = False

        while True:
            frog_idx = get_first_R_idx(start_idx, frogs) if frog_to_move == 'R' else get_last_F_idx(start_idx, frogs)
            if frog_idx is None:  # no more frogs to move
                return

            move_index = can_move(frog_idx, frogs)
            if type(move_index) is int:
                break  # move the frog
            start_idx -= FROG_DIRECTIONS[frogs[frog_idx]]

            if 0 > start_idx > len(frogs):
                return  # out of bounds

        swap_frog(move_index, frog_idx, frogs)
        start_idx = frog_idx


def swap_frog(idx, idx2, frogs):
    """ Moves a frog, switching it's position with the given index """
    temp = frogs[idx]
    frogs[idx] = frogs[idx2]
    frogs[idx2] = temp


def get_first_R_idx(start, frogs):
    """ returns the index of the first R frog from start index"""
    for idx in range(start, len(frogs)):
        if frogs[idx] == 'R':
            return idx


def get_last_F_idx(end, frogs):
    """ returns the index of the last F frog from start index"""
    for idx in range(end, -1, -1):
        if frogs[idx] == 'F':
            return idx


def can_move(idx, frogs):
    """
    A frog can move if the index next to it is free - '_', or if there is a frog in front of it and a space
    after the frog, essentially jumping over the frog. - 'F''R''_' - F can jump over R to get to the spot
    F frogs can only move right, while R frogs can only move left
    Returns values depending on if the frog at the given index can move.
    returns 'False' if it can't
    returns the index to which it can move, if it can
    """
    given_frog = frogs[idx]
    neighbour_idx = idx + FROG_DIRECTIONS[given_frog]
    further_neighbour_idx = neighbour_idx + FROG_DIRECTIONS[given_frog]

    if 0 <= neighbour_idx < len(frogs) and frogs[neighbour_idx] == '_':
        return neighbour_idx
    elif 0 <= further_neighbour_idx < len(frogs) and frogs[further_neighbour_idx] == '_':
        # jumps over a frog
        return further_neighbour_idx

    # Other frog there or out of bounds
    return 'False'

if __name__ == '__main__':
    main()