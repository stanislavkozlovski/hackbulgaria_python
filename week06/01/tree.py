class Node:
    def __init__(self, value, parent: 'Node'=None):
        self.parent = parent
        self.children = []  # type ['Node']
        self.value = value

    def add_child(self, child):
        self.children.append(child)


class Tree:
    def __init__(self, root):
        self.root = Node(root)
        self.nodes = 0
        self.max_height = 0

    def add_child(self, parent, child):
        """ Adds a child to the given parent.
        Assumes that the parent exists"""
        wanted_parent = self.__find(parent, self.root)

        # check if there isn't a child with that value already
        child_exists = self.__find(child, self.root)
        if child_exists:
            raise Exception('A child with value {} already exists!'.format(child))
        
        wanted_parent.add_child(Node(child, parent=wanted_parent))
        self.nodes += 1

    def __find(self, x, parent: 'Node'):
        """ Searched the tree for a value and returns its index"""
        found = None
        if parent.value == x:
            return parent

        for child in parent.children:
            if child.value == x:
                return child
            new_found = self.__find(x, parent=child)
            if new_found:
                found = new_found

        return found

    def find(self, x):
        return bool(self.__find(x, self.root))

    def height(self):
        def __count_height(parent=self.root, height=0):
            """ Counts the maximum height from the given parent"""
            if height > self.max_height:
                self.max_height = height
            for child in parent.children:
                __count_height(parent=child, height=height+1)

        __count_height()
        return self.max_height

    def count_nodes(self):
        return self.nodes

    def tree_levels(self):
        levels_dict = {0: [self.root.value]}  # keep the levels in a dict for easier storage

        def __fill_levels_dict(parent=self.root, height=1):
            """ Traverse the tree, keeping record of what height we're at.
                Also add each node at the current level in the appropriate key in the dictionary """
            if not parent.children:
                return  # we've already added the parent to the appropriate level
            elif height not in levels_dict:
                levels_dict[height] = []
            for child in parent.children:
                levels_dict[height].append(child.value)  # add to the levels dict
                __fill_levels_dict(parent=child, height=height+1)  # recursively traverse

        __fill_levels_dict()
        # convert the dictionary to a tree
        tree_levels = [levels_dict[level] for level in sorted(list(levels_dict.keys()))]
        return tree_levels

    def consecutive_tree_levels(self):
        """ returns a list of the tree's contents, listed consecutively.
        [a, a.b, a.c, b, b.b]"""
        lst = [self.root.value]

        def __fill_consecutive_tree_levels(parent=self.root):
            """ Fills a list of consecutive connections in it, in other words,
                traverses a tree from left to right                       """
            for child in parent.children:
                lst.append(child.value)
                __fill_consecutive_tree_levels(parent=child)  # call recursively

        __fill_consecutive_tree_levels()
        return lst

#
# tr = Tree(3)
# tr.add_child(3,5)
# print(tr.find(5))
# print(tr.find(10))
# print(tr.height())
# tr.add_child(5, 3)
# tr.add_child(5,4)
# print(tr.height())
# print(tr.tree_levels())
# print(tr.consecutive_tree_levels())
