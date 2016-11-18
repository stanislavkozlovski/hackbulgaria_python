import unittest

from binary_search import find_turning_point

class FindTurningPointTests(unittest.TestCase):

    def test_start_turning_point(self):
        test = [4,1,2]
        self.assertEqual(find_turning_point(test, 0, len(test)), 1)

    def test_end_turning_point(self):
        test = [1, 2, 4, 3]
        self.assertEqual(find_turning_point(test, 0, len(test)), 3)

    def test_turning_point(self):
        test = [10, 20, 30, 40, 10]
        self.assertEqual(find_turning_point(test, 0, len(test)), 4)

        test = [10, 20, 30, 20, 10]
        self.assertEqual(find_turning_point(test, 0, len(test)), 3)

        test = [10, 20, 19, 18, 10]
        self.assertEqual(find_turning_point(test, 0, len(test)), 2)

        test = [10, 9, 8, 7, 6]
        self.assertEqual(find_turning_point(test, 0, len(test)), 1)

if __name__ == '__main__':
    unittest.main()