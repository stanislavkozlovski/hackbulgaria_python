import unittest
import sys
from io import StringIO
from controllers.main import read_spell, Cinema


class MainControllerTests(unittest.TestCase):
    def setUp(self):
        self.cinema = Cinema()

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
            read_spell(self.cinema)
            self.assertTrue(expected_output in output.getvalue())
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__

    def test_show_movie_projections(self):
        user_input = "show movie projections 2"
        expected_output = """Projections for movie 'Wreck it-Ralph':
[6] - 2014-04-02 19:30 (2D) - 100 Free Spots
[5] - 2014-04-02 22:00 (3D) - 98 Free Spots"""
        output = StringIO()
        try:
            sys.stdin = StringIO(user_input)
            sys.stdout = output
            read_spell(self.cinema)
            self.assertTrue(expected_output in output.getvalue())
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__

    def test_show_movie_projections_with_date(self):
        user_input = "show movie projections 1 2014-04-01"
        expected_output = """Projections for movie 'The Hunger Games: Catching Fire' on date 2014-04-01:
[2] - 19:00 (2D) - 100 Free Spots
[1] - 19:10 (3D) - 97 Free Spots"""
        output = StringIO()
        try:
            sys.stdin = StringIO(user_input)
            sys.stdout = output
            read_spell(self.cinema)
            self.assertTrue(expected_output in output.getvalue())
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__

    def test_show_movie_projections_valid_movie_invalid_date(self):
        """ There are no movie projections on the given date"""
        user_input = "show movie projections 1 2014-12-31"
        expected_output = """Projections for movie 'The Hunger Games: Catching Fire' on date 2014-12-31:"""
        output = StringIO()
        try:
            sys.stdin = StringIO(user_input)
            sys.stdout = output
            read_spell(self.cinema)
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
            read_spell(self.cinema)
            self.assertTrue(expected_output in output.getvalue())
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__

    def test_show_movie_projections_invalid_date(self):
        user_input = "show movie projections 1 2014-02-31"
        expected_output = 'Invalid date! Date should be in the format of YYYY-MM-DD!'
        output = StringIO()
        try:
            sys.stdin = StringIO(user_input)
            sys.stdout = output
            read_spell(self.cinema)
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
            read_spell(self.cinema)
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
            read_spell(self.cinema)
            self.assertTrue(expected_output in output.getvalue())
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__


if __name__ == '__main__':
    unittest.main()
