""" Unit tests for the utility functions """
import unittest
from settings import utils


class UtilsTests(unittest.TestCase):
    def test_create_movie_hall_representation(self):
        """
        The function should return a 11x11 matrix, representing each row/col number
        """
        matrix = utils.create_movie_hall_matrix_representation()
        self.assertEqual(len(matrix), 11)
        for idx, row in enumerate(matrix[1:]):
            self.assertEqual(row[0], str(idx+1))
            self.assertEqual(len(row), 11)


if __name__ == '__main__':
    unittest.main()
