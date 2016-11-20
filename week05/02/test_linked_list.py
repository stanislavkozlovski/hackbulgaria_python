import unittest
from recursive_linked_list import LinkedList


class LinkedListTest(unittest.TestCase):

    def setUp(self):
        self.ll = LinkedList()

    def test_adding_element(self):
        self.ll.add_element(4)
        self.assertEqual(self.ll.size(), 1)

    def test_remove_element(self):
        self.ll.add_element(4)
        size = self.ll.size()
        self.ll.remove(0)
        size2 = self.ll.size()
        self.assertFalse(size == size2)

    def test_getting_index(self):
        node = self.ll.get_index(0)
        self.assertEqual(node, None)
        self.ll.add_element(1)
        self.ll.add_element(1)
        self.ll.add_element(1)

        self.assertEqual(self.ll.get_index(2).value, 1)
        self.assertEqual(self.ll.get_index(3), None)

    def test_remove(self):
        self.assertEqual(self.ll.remove(-1), None)
        self.assertEqual(self.ll.remove(0), None)
        self.assertEqual(self.ll.remove(1), None)
        self.assertEqual(self.ll.remove(1232), None)
        self.ll.add_element(1)
        self.assertEqual(self.ll.remove(0), True)
        self.assertEqual(self.ll.remove(1), None)
        self.ll.add_element(1)
        self.ll.add_element(1)
        self.assertEqual(self.ll.remove(1), True)
        self.assertEqual(self.ll.size(), 1)

    def test_to_list(self):
        self.ll.add_element(1)
        self.ll.add_element(2)
        self.ll.add_element(3)
        self.assertEqual(self.ll.to_list(), [1,2,3])

    def test_add_at_index(self):
        # invalid indexes
        self.assertEqual(self.ll.add_at_index(123, 2), False)
        self.assertEqual(self.ll.add_at_index(-1, 2), False)
        self.assertEqual(self.ll.add_at_index(1, 2), False)
        self.assertEqual(self.ll.add_at_index(0, 2), None)
        self.assertEqual(self.ll.add_at_index(1, 2), None)

    def test_add_first(self):
        self.ll.add_first(12)
        self.assertEqual(self.ll.head.value, 12)  # add first on empty list
        self.ll.add_first(13)
        self.assertEqual(self.ll.head.value, 13)
        self.assertEqual(self.ll.tail.value, 12)  # check tail after adding a first value

    def test_add_list(self):
        # add lists and check the expected values
        self.ll.add_list([1,2,3])
        self.assertEqual(self.ll.head.value, 1)
        self.assertEqual(self.ll.get_index(1).value, 2)
        self.assertEqual(self.ll.tail.value, 3)
        # add another list
        self.ll.add_list([1,2,3])
        self.assertEqual(self.ll.head.value, 1)
        self.assertEqual(self.ll.get_index(4).value, 2)
        self.assertEqual(self.ll.tail.value, 3)

    def test_add_linked_list(self):
        # create a new list
        new_ll = LinkedList()
        new_ll.add_element(1)
        new_ll.add_element(2)
        new_ll.add_element(3)
        self.ll.add_element(0)
        self.ll.add_linked_list(new_ll)
        self.assertEqual(self.ll.head.value, 0)
        self.assertEqual(self.ll.tail.value, 3)
        self.assertEqual(self.ll.to_list(), [0,1,2,3])

    def test_ll_from_to(self):
        """get a part of the linked list as a new linked list"""
        self.ll.add_list([0,1,2,3,4,5,6,7,8])
        new_ll = self.ll.ll_from_to(0,4)
        self.assertEqual(new_ll.head.value, 0)
        self.assertEqual(new_ll.tail.value, 4)
        self.assertEqual(new_ll.to_list(), [0,1,2,3, 4])

    def test_pop(self):
        """pop removes the last value from the list"""
        self.ll.add_list([0,1,2,3,4])
        self.assertEqual(self.ll.tail.value, 4)
        self.ll.pop()
        self.assertEqual(self.ll.tail.value, 3)
        self.ll.pop()
        self.assertEqual(self.ll.tail.value, 2)
        self.ll.pop()
        self.assertEqual(self.ll.tail.value, 1)
        self.ll.pop()
        self.assertEqual(self.ll.tail.value, 0)
        self.assertFalse(self.ll.pop())  # should return false when there are no more elements left

    def test_reduce_to_unique(self):
        """ reduce to unique returns a linked list with no repeating values in it"""
        orig_list = [0,0,1,0,0,1,2,3,2]
        expected_list = [0,1,2,3]
        self.ll.add_list(orig_list)
        self.assertEqual(self.ll.to_list(), orig_list)
        unique_ll = self.ll.reduce_to_unique()
        self.assertNotEqual(unique_ll.to_list(), orig_list)
        self.assertEqual(unique_ll.to_list(), expected_list)


if __name__ == '__main__':
    unittest.main()