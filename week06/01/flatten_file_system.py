import os
from tree import Tree

def flatten_file_system1(path: str):
    file_system = Tree(path)

    def __fill_file_system(path_=path):
        for file in os.scandir(path_):
            file_system.add_child(path_, file.path)
            if file.is_dir():
                __fill_file_system(path_=file.path)

    __fill_file_system()

    return [item for sublist in sorted(file_system.tree_levels()) for item in sublist]

def flatten_file_system2(path: str):
    file_system = Tree(path)

    def __fill_file_system(path_=path):
        for file in os.scandir(path_):
            file_system.add_child(path_, file.path)
            if file.is_dir():
                __fill_file_system(path_=file.path)
    __fill_file_system()

    return file_system.consecutive_tree_levels()



print(flatten_file_system1('/home/netherblood/PycharmProjects/hackbulgaria_python/week01/1-First-Steps-In-Python'))
print(flatten_file_system2('/home/netherblood/PycharmProjects/hackbulgaria_python/week01/1-First-Steps-In-Python'))