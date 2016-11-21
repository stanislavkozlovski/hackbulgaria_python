import os
from tree import Tree


def flatten_file_system1(path: str):
    file_system = Tree(path)

    __fill_file_system(file_system, path)
    # converts the tree_levels() result that is a list of lists, holding at each index the files that are on that level
    # into a single list
    return [item for sublist in sorted(file_system.tree_levels()) for item in sublist]


def flatten_file_system2(path: str):
    file_system = Tree(path)

    __fill_file_system(file_system, path)

    return file_system.consecutive_tree_levels()


def __fill_file_system(file_system: 'Tree', path):
    """ Fills our Tree with the files under the given path recursively"""
    for file in os.scandir(path):
        file_system.add_child(path, file.path)
        if file.is_dir():
            __fill_file_system(file_system, path=file.path)  # continue recursively downwards

print(flatten_file_system1('/home/netherblood/PycharmProjects/hackbulgaria_python/week01/1-First-Steps-In-Python'))
print(flatten_file_system2('/home/netherblood/PycharmProjects/hackbulgaria_python/week01/1-First-Steps-In-Python'))