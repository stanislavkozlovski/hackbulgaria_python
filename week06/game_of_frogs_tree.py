FROG_DIRECTION = {'>': 1, '<': -1}


class TreeNode:
    def __init__(self, value: tuple, parent: 'TreeNode'=None):
        self.value = value
        self.parent = parent
        # self.children = children


def number_of_frogs(count: int):
    root_value = tuple(['>'] * count + ['_'] + ['<'] * count)
    expected_value = tuple(['<'] * count + ['_'] + ['>'] * count)
    tree = TreeNode(value=root_value)
    right_node = create_children(tree, expected_value)
    print(build_path(right_node))  # get the done path

def build_path(start_node):
    path = []
    while True:
        path.append(''.join(start_node.value))
        if not start_node.parent:
            break
        start_node = start_node.parent
    return list(reversed(path))


def create_children(node, expected_frogs) -> TreeNode:
    should_stop, right_node, wrong_solutions = False, None, set()
    expected_frogs = expected_frogs
    max_range = len(node.value) - 1

    def __create_children(node):
        nonlocal should_stop, right_node, wrong_solutions, expected_frogs
        can_move = False
        if node.value in wrong_solutions:
            return
        for frog_idx, frog in enumerate(node.value):
            if should_stop:
                return

            target_index = frog_can_move(frogs=node.value, frog_index=frog_idx, max_range=max_range)

            if target_index is None:
                continue
            can_move = True  # we can move the frog

            moved_frogs = move_frog(frogs=node.value, source_index=frog_idx, target_index=target_index)
            new_node = TreeNode(value=moved_frogs, parent=node)

            if moved_frogs == expected_frogs:
                # we've found the solution
                should_stop = True
                right_node = new_node
                return

            # node.children.append(new_node)
            __create_children(new_node)  # recursively call the function using the new node
        if not can_move:
            wrong_solutions.add(node.value)
    __create_children(node)
    return right_node


def move_frog(frogs: tuple, source_index, target_index):
    """ Swaps the frogs """
    temp_list = list(frogs)

    # swap the values
    temp_list[source_index], temp_list[target_index] = temp_list[target_index], temp_list[source_index]

    return tuple(temp_list)


def frog_can_move(frogs, frog_index, max_range):
    frog = frogs[frog_index]
    if frog != '_':
        next_index = frog_index + FROG_DIRECTION[frog]
        if 0 <= next_index <= max_range:  # in bounds
            if frogs[next_index] == '_':
                return next_index

            nexter_index = next_index + FROG_DIRECTION[frog]
            if 0 <= nexter_index <= max_range:  # in bounds
                if frogs[nexter_index] == '_':
                    return nexter_index


import time
start = time.time()
number_of_frogs(3)
end = time.time()
print(end-start)
">><<_"