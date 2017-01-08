import unittest
import sys
from io import StringIO
from controllers.main import read_spell, Cinema
from settings.constants import DB_USERS_USERNAME_KEY


class MainControllerTests(unittest.TestCase):
    def setUp(self):
        self.cinema = Cinema()
        self.valid_username = "Rositsa Zlateva"
        self.valid_username2 = "Slavyana Monkova"
        self.valid_password = "rosata"
        self.valid_password2 = "slavyana"

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

    def test_valid_login(self):
        user_input = "{name}\n{pwd}".format(name=self.valid_username, pwd=self.valid_password)
        expected_output = "You have been successfully logged in as Rositsa Zlateva!"
        output = StringIO()
        try:
            sys.stdin = StringIO(user_input)
            sys.stdout = output
            self.cinema.log_user_in()
            self.assertTrue(expected_output in output.getvalue())
            self.assertEqual(self.cinema.user[DB_USERS_USERNAME_KEY], self.valid_username)
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__

    def test_invalid_log_in(self):
        user_input = "{name}\n{pwd}\nNo".format(name=self.valid_username, pwd='aAaa')
        expected_output = "Invalid username/password! Would you like to log in again?(y/n)"
        output = StringIO()
        try:
            sys.stdin = StringIO(user_input)
            sys.stdout = output
            self.cinema.log_user_in()
            self.assertTrue(expected_output in output.getvalue())
            self.assertIsNone(self.cinema.user)
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__

    def test_double_log_in_decline_logout(self):
        """ The cinema should prompt you to log out with your old user """
        user_input = "{name}\n{pwd}\nNo".format(name=self.valid_username, pwd=self.valid_password)
        expected_output_1 = "You have been successfully logged in as Rositsa Zlateva!"
        expected_output_2 = "You are already logged in as {name}. Would you like to log out?".format(name=self.valid_username)
        output = StringIO()
        try:
            sys.stdin = StringIO(user_input)
            sys.stdout = output
            self.cinema.log_user_in()
            self.assertTrue(expected_output_1 in output.getvalue())
            self.cinema.log_user_in()
            self.assertTrue(expected_output_2 in output.getvalue())
            # validate that we're still logged in as Rositsa
            self.assertEqual(self.cinema.user[DB_USERS_USERNAME_KEY], self.valid_username)
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__

    def test_double_log_in_accept_logout(self):
        """ The cinema should prompt you to log out with your old user. We log out and log in with a new user. """
        user_input = "{name}\n{pwd}\nYes\n{new_name}\n{new_pwd}".format(
            name=self.valid_username, pwd=self.valid_password,
            new_name=self.valid_username2, new_pwd=self.valid_password2)
        expected_output_1 = "You have been successfully logged in as Rositsa Zlateva!"
        expected_output_2 = "You are already logged in as {name}. Would you like to log out?(y/n)".format(
            name=self.valid_username)
        output = StringIO()
        try:
            sys.stdin = StringIO(user_input)
            sys.stdout = output
            self.cinema.log_user_in()
            self.assertTrue(expected_output_1 in output.getvalue())
            self.cinema.log_user_in()
            self.assertTrue(expected_output_2 in output.getvalue())
            self.assertTrue(expected_output_1 in output.getvalue())
            # validate that we're still logged in as Slavyana
            self.assertEqual(self.cinema.user[DB_USERS_USERNAME_KEY], self.valid_username2)
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__

    def test_double_log_in_accept_logout_invalid_log_in(self):
        """ The cinema should prompt you to log out with your old user. We log out and log in with a new user. """
        """ The cinema should prompt you to log out with your old user """
        user_input = "{name}\n{pwd}\nYes\n{new_name}\n{new_pwd}\nNo".format(
            name=self.valid_username, pwd=self.valid_password,
            new_name=self.valid_username2, new_pwd='aAa')
        expected_output_1 = "You have been successfully logged in as Rositsa Zlateva!"
        expected_output_2 = "You are already logged in as {name}. Would you like to log out?(y/n)".format(
            name=self.valid_username)
        expected_output_3 = "Invalid username/password! Would you like to log in again?(y/n)"

        output = StringIO()
        try:
            sys.stdin = StringIO(user_input)
            sys.stdout = output
            self.cinema.log_user_in()
            self.assertTrue(expected_output_1 in output.getvalue())
            self.cinema.log_user_in()
            self.assertTrue(expected_output_2 in output.getvalue())
            self.assertTrue(expected_output_3 in output.getvalue())

            # validate that we're not logged in
            self.assertIsNone(self.cinema.user)
        finally:
            sys.stdin = sys.__stdin__
            sys.stdout = sys.__stdout__

if __name__ == '__main__':
    unittest.main()
