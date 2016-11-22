import unittest
from game_of_frogs import line_up_frogs

class Tests(unittest.TestCase):

    def test_line_up_frogs_one(self):
        frogs = ['F', '_', 'R']
        expected_output = ['R', '_', 'F']
        self.assertEqual(line_up_frogs(frogs, 1, expected_output), expected_output)

    def test_line_up_frogs_two(self):
        frogs = ['F', 'F', '_', 'R', 'R']
        expected_output = ['R', 'R', '_', 'F', 'F']
        self.assertEqual(line_up_frogs(frogs, 2, expected_output), expected_output)

    def test_line_up_frogs_three(self):
        frogs = ['F'] * 3 + ['_'] + ['R'] * 3
        expected_output = ['R', 'R', 'R', '_', 'F', 'F', 'F']
        self.assertEqual(line_up_frogs(frogs, 3, expected_output), expected_output)

    def test_line_up_frogs_four(self):
        frogs = ['F'] * 4 + ['_'] + ['R'] * 4
        expected_output = ['R', 'R', 'R', 'R', '_', 'F', 'F', 'F', 'F']
        self.assertEqual(line_up_frogs(frogs, 4, expected_output), expected_output)

    def test_line_up_frogs_three_hundred(self):
        frogs = ['F'] * 300 + ['_'] + ['R'] * 300
        expected_output = ['R'] * 300 + ['_'] + ['F'] * 300
        self.assertEqual(line_up_frogs(frogs, 300, expected_output), expected_output)

if __name__ == '__main__':
    unittest.main()