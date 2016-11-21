import unittest
from game_of_frogs import line_up_frogs

class Tests(unittest.TestCase):

    def test_line_up_frogs_one(self):
        frogs = ['F', '_', 'R']
        self.assertEqual(line_up_frogs(frogs, 1), ['R', '_', 'F'])

    def test_line_up_frogs_two(self):
        frogs = ['F', 'F', '_', 'R', 'R']
        self.assertEqual(line_up_frogs(frogs, 2), ['R', 'R', '_', 'F', 'F'])

    def test_line_up_frogs_three(self):
        frogs = ['F'] * 3 + ['_'] + ['R'] * 3
        self.assertEqual(line_up_frogs(frogs, 3), ['R', 'R', 'R', '_', 'F', 'F', 'F'])

    def test_line_up_frogs_four(self):
        frogs = ['F'] * 4 + ['_'] + ['R'] * 4
        self.assertEqual(line_up_frogs(frogs, 4), ['R', 'R', 'R', 'R', '_', 'F', 'F', 'F', 'F'])

    def test_line_up_frogs_three_hundred(self):
        frogs = ['F'] * 300 + ['_'] + ['R'] * 300
        self.assertEqual(line_up_frogs(frogs, 300), ['R'] * 300 + ['_'] + ['F'] * 300)

if __name__ == '__main__':
    unittest.main()