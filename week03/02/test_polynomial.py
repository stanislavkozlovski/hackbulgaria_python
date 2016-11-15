import unittest
from subprocess import check_output


def call_solution(arg):
    command = "python3 polynomials_and_derivatives.py {}".format(arg)

    return check_output(["/bin/bash", "-c", command])\
        .decode('utf-8').strip()


class TestPolynomial(unittest.TestCase):
    def test_poly_with_repeating_power(self):
        expected = """The derivative of f(x) = 2x^3 + 3x^2 + x is:
f'(x) = 6x^2 + 6x + 1""".strip()

        output = call_solution("x+x^2+2x^2+2x^3")

        self.assertEqual(output, expected)

    def test_poly_only_with_free_member(self):
        expected = """The derivative of f(x) = 8 is:
f'(x) = 0""".strip()

        output = call_solution("8")

        self.assertEqual(output, expected)

    def test_poly_only_with_x(self):
        expected = """The derivative of f(x) = x is:
f'(x) = 1""".strip()

        output = call_solution("x")
        self.assertEqual(output, expected)

    def test_poly_with_x_and_free_member(self):
        expected = """The derivative of f(x) = 2x^2 + 1 is:
f'(x) = 4x""".strip()

        output = call_solution("2x^2+1")
        self.assertEqual(output, expected)

    def test_poly_with_free_number_0(self):
        expected = """The derivative of f(x) = x is:
f'(x) = 1""".strip()

        output = call_solution("x+0")
        self.assertEqual(output, expected)


if __name__ == '__main__':
    unittest.main()
