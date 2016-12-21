import unittest
import sys
from io import StringIO
from controllers.main import read_spell


class MainControllerTests(unittest.TestCase):
    def test_show_movies(self):
        expected_output = """Current movies:
[1] - The Hunger Games: Catching Fire (7.9)
[2] - Wreck-It Ralph (7.8)
[3] - Her (8.3)"""
        input = "show movies"
        output = StringIO()
        try:
            sys.stdin = StringIO(input)
            sys.stdout = output
            read_spell()
            self.assertTrue(expected_output in output.getvalue())
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__

    def test_invalid_command_once(self):
        expected_output = "Invalid spell!"
        input = "show kookies\nshow movies"
        output = StringIO()
        try:
            sys.stdin = StringIO(input)
            sys.stdout = output
            read_spell()
            self.assertTrue(expected_output in output.getvalue())
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__

    def test_invalid_commands_multiple_times(self):
        expected_output = "Invalid spell!\nInvalid spell!\nInvalid spell!\n"
        input = "sfaa\nfafa\nfafa\nshow movies"
        output = StringIO()
        try:
            sys.stdin = StringIO(input)
            sys.stdout = output
            read_spell()
            self.assertTrue(expected_output in output.getvalue())
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__


if __name__ == '__main__':
    unittest.main()