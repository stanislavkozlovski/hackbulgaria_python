import unittest
import sys
from io import StringIO
from controllers.main import read_spell


class MainControllerTests(unittest.TestCase):
    def test_show_movies(self):
        expected_output = """Current movies:
[3] - Her (8.3)
[1] - The Hunger Games: Catching Fire (7.9)
[2] - Wreck it-Ralph (7.8)"""

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

    def test_show_movie_projections(self):
        input = "show movie projections 2"
        expected_output = """Projections for movie 'Wreck-It Ralph':
[5] - 2014-04-02 19:30 (2D)
[6] - 2014-04-02 22:00 (3D)"""
        output = StringIO()
        try:
            sys.stdin = StringIO(input)
            sys.stdout = output
            read_spell()
            self.assertTrue(expected_output in output.getvalue())
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__

    def test_show_movie_projections_with_date(self):
        input = "show movie projections 1 2014-04-01"
        expected_output = """Projections for movie 'The Hunger Games: Catching Fire' on date 2014-04-01:
[1] - 19:00 (3D)
[2] - 19:10 (2D)"""
        output = StringIO()
        try:
            sys.stdin = StringIO(input)
            sys.stdout = output
            read_spell()
            self.assertTrue(expected_output in output.getvalue())
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__

    def test_show_movie_projections_invalid_movie(self):
        input = "show movie projections 4"
        expected_output = """Invalid movie id!"""
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