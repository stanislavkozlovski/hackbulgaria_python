from copy import deepcopy

class Node:
    def __init__(self, value, index: int, next_node: 'Node'=None, prev_node: 'Node'=None):
        self.value = value
        self.next = next_node
        self.prev = prev_node
        self.index = index

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = self.head
        self.list_size = 0

    def add_element(self, data):
        if self.head and self.tail:
            old_tail = self.tail
            self.list_size += 1
            # our tail is now the latest element
            new_tail = Node(data, next_node=None, prev_node=old_tail, index=old_tail.index+1,)
            old_tail.next = new_tail  # our tail now has a next element
            self.tail = new_tail  # replace tail
        elif self.head: # self.tail is None
            self.tail = Node(data, next_node=None, prev_node=self.head, index=1)
            self.head.next = self.tail
            self.list_size += 1
        else: # adding first element
            self.add_first(data)

    def get_index(self, index):
        if self.list_size == 0 or index < 0 or index >= self.list_size:
            print('Invalid index!')
        else:
            return self.__get_index(index, self.head)

    def __get_index(self, index, current_node):
        if current_node.index == index:
            return current_node

        return self.__get_index(index, current_node.next)

    def size(self):
        return self.list_size

    def remove(self, index):
        # get the previous and next node to the one we want to remove, then simply link the previous to the next
        # effectively cutting the one we want to remove
        if self.list_size == 0 or index < 0 or index >= self.list_size:
            return

        if index == 0:
            node_to_remove = self.head
            node_after = node_to_remove.next
            self.head = node_after  # remove the head
        else:
            # link the previous node to the node after
            prev_node = self.get_index(index-1)
            node_to_remove = prev_node.next
            node_after = node_to_remove.next
            prev_node.next = node_after
            if index == self.tail.index:
                # we're removing the last node, therefore we need to give it a new tail
                self.tail = prev_node

        # fix the indexes of every element after
        if node_after:
            self.__modify_indexes_from_node_to_end(node_after, -1)  # decrement each node after's index

        self.list_size -= 1
        return True

    def remove_last(self):
        """ remove the last element in the linked list"""
        # make the new tail the previous element
        self.tail = self.tail.prev
        self.tail.next = None

    def pprint(self, start_node: 'Node'):
        if start_node.next:
            print("{val}->".format(val=start_node.value), end='')
            self.pprint(start_node.next)
        else:
            print("{val}".format(val=start_node.value), end='')
            print()  # new line

    def to_list(self, lst: list=[], node='start'):
        if not node:
            return lst
        if node == 'start' and self.head:
            lst = []
            node = self.head

        lst.append(node.value)
        return self.to_list(lst, node.next)


    def add_at_index(self, index, data):
        if (self.list_size == 0 and index == 0) or index == 0:
            self.add_first(data)
        elif index < 0 or index > self.list_size:
            return False
        elif index == self.list_size:
            # add at the end
            self.add_element(data)
        else:
            '''add somewhere in the middle'''
            # get element before index
            prev_node = self.get_index(index-1)
            node_at_index = prev_node.next  # the element at index we're replacing

            new_node = Node(value=data, index=index, next_node=node_at_index, prev_node=prev_node)  # new node points to the original element
            node_at_index.prev=new_node  # original node is now after our new node
            self.__modify_indexes_from_node_to_end(node_at_index.next, 1) # increment the indexes of each node after
            prev_node.next = new_node  # prev node now points to the new node
            self.list_size += 1

    def add_first(self, data):
        if self.head and self.tail:
            old_head = self.head
            # fix indexes of nodes onwards
            self.__modify_indexes_from_node_to_end(old_head, 1)
            new_head = Node(value=data, index=0, next_node=old_head, prev_node=None)
            old_head.prev = new_head
            self.head = new_head  # change head
            self.list_size += 1
        elif self.head:  # Tail is empty
            self.tail = self.head  # our head becomes our tail
            # create new head
            self.head = Node(value=data, index=0, next_node=self.tail, prev_node=None)
            self.tail.prev = self.head
        else:
            # adding the first ever element
            self.head = Node(value=data, index=0, next_node=self.tail, prev_node=None)
            self.tail = None
            self.list_size += 1

    def add_last(self, data):
        """ Add an element at the end"""
        self.add_element(data)

    def __modify_indexes_from_node_to_end(self, node, change):
        """
        Modifies the indexes of every node from (and including) the start node to the end of the linked list.
        Useful for when you add/remove an element in the middle of the list, because you need to change the
        next nodes' indexes accordingly
        :param change: Can either be 1 or -1, depending if we want to increment or decrement the index
        """
        if not node:
            return
        node.index += change
        self.__modify_indexes_from_node_to_end(node.next, change)

    def add_list(self, list_to_add: list):
        for el in list_to_add:
            self.add_element(el)

    def add_linked_list(self, linked_list: 'LinkedList'):
        self.add_list(linked_list.to_list())

    def ll_from_to(self, start_index, end_index):
        new_ll_head = self.get_index(start_index)
        new_ll = LinkedList()
        new_ll.add_element(new_ll_head.value)
        return LinkedList.add_to_new_ll_nodes(new_ll, new_ll_head.next, end_index)

    @staticmethod
    def add_to_new_ll_nodes(linked_list: 'LinkedList', node: 'Node', end_index: int):
        linked_list.add_element(node.value)
        if node.index == end_index:
            return linked_list
        else:
            return LinkedList.add_to_new_ll_nodes(linked_list, node.next, end_index)

    def pop(self):
        if self.tail:
            self.remove(self.tail.index)
        elif self.head:  # linked list has only one element
            self.head = None
            self.size -= 1
        else:
            return False  # No elements in our LinkedList

    def reduce_to_unique(self):
        self_list = self.to_list()
        unique_elements = set(self_list)
        # they are no unordered, transform them into a list that is ordered like the original
        # by rebuilding the list
        unique_list = []
        for el in self_list:
            if el in unique_elements:  # get the element only if it's in our unique elements
                unique_elements.remove(el)  # once we've got it, remove it so as to not get it again on repeat
                unique_list.append(el)
        # what we have now is an ordered unique version of our original list
        # create the new unique linked list
        new_ll = LinkedList()
        new_ll.add_list(unique_list)
        return new_ll


# ll = LinkedList()
# ll.add_element(1)
# ll.add_element(2)
# ll.add_element(3)
# ll.add_element(4)
# ll.pprint(start_node=ll.head)
# # 1-2-3-4
# ll.remove(2)
# ll.pprint(start_node=ll.head)
# # 1-2-4
# print(ll.to_list())
# #[1,2,4]
# ll.add_at_index(1, 10)
# ll.pprint(start_node=ll.head)
# # 1-10-2-4
# ll.add_first(55)
# ll.pprint(start_node=ll.head)
# # 55-1-10-2-4
# ll.add_list([5,5,5])
# ll.pprint(start_node=ll.head)
# # 55-1-10-2-4-5-5-5
# ll.pop()
# ll.pprint(start_node=ll.head)
# # 55-1-10-2-4-5-5
# ll.ll_from_to(2, 4).pprint(start_node=ll.head)
# # 10-2-4
# ll.add_list([1,2])
# ll.pprint(start_node=ll.head)
# # 55-1-10-2-4-5-5-1-2
# unique_ll = ll.reduce_to_unique()
# unique_ll.pprint(start_node=ll.head)
# # 55-1-10-2-4-5