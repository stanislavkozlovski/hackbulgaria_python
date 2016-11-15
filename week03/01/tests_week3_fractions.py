import unittest
from fractions import Fraction


class TestFractions(unittest.TestCase):
    def setUp(self):
        self.fraction1 = Fraction(1, 2)
        self.fraction2 = Fraction(2, 4)

    def test_str(self):
        self.assertEqual(str(self.fraction1), "1 / 2")

    # def test_equal(self):
        # self.assertTrue(self.fraction1 == self.fraction2)

    def test_plus(self):
        self.assertEqual(self.fraction1 + self.fraction2, 1)






if __name__ == '__main__':
    unittest.main()