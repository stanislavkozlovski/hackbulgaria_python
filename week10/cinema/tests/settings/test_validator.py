import unittest
from settings.validator import is_valid_spell, is_valid_date, is_valid_ticket_count, is_valid_row_or_col


class ValidatorTests(unittest.TestCase):
    def test_is_valid_spell_valid_spell(self):
        self.assertTrue(is_valid_spell("show movies"))

    def test_is_valid_spell_invalid_spell(self):
        self.assertFalse(is_valid_spell("show kookies"))

    def test_is_valid_spell_int(self):
        self.assertFalse(is_valid_spell(5))

    # --------------DATE VALIDATOR--------------
    def test_is_valid_date_valid_date(self):
        self.assertTrue(is_valid_date("2014-10-31"))

    def test_is_valid_date_no_padding_zero(self):
        """Should be valid"""
        self.assertTrue(is_valid_date("2016-2-1"))

    def test_is_valid_date_invalid_day(self):
        self.assertFalse(is_valid_date("2016-02-31"))

    def test_is_valid_date_invalid_month(self):
        self.assertFalse(is_valid_date("2016-13-31"))

    def test_is_valid_date_negative_month(self):
        self.assertFalse(is_valid_date("2016--2-31"))

    def test_is_valid_date_none_month(self):
        self.assertFalse(is_valid_date(None))

    def test_is_valid_date_number(self):
        self.assertFalse(is_valid_date(20160231))

    def test_is_valid_date_empty_str(self):
        self.assertFalse(is_valid_date(""))

    # --------------TICKET COUNT VALIDATOR--------------
    def test_ticket_count_validator_valid_count(self):
        self.assertTrue(is_valid_ticket_count('5'))
        self.assertTrue(is_valid_ticket_count('1'))
        self.assertTrue(is_valid_ticket_count('10'))

    def test_ticket_count_validator_invalid_count(self):
        """ Valid tickets are between 1 and 10"""
        self.assertFalse(is_valid_ticket_count('11'))
        self.assertFalse(is_valid_ticket_count('0'))
        self.assertFalse(is_valid_ticket_count('-1'))
        self.assertFalse(is_valid_ticket_count('1434019341049132'))

    def test_ticket_count_validator_invalid_number(self):
        self.assertFalse(is_valid_ticket_count('1.212'))
        self.assertFalse(is_valid_ticket_count('1.21e2'))
        self.assertFalse(is_valid_ticket_count('The Real is on the Rise'))
        self.assertFalse(is_valid_ticket_count(''))
        self.assertFalse(is_valid_ticket_count('\n\t\r'))
        self.assertFalse(is_valid_ticket_count(None))

    # --------------ROW/COL VALIDATOR--------------
    def test_row_or_col_validator_valid_count(self):
        self.assertTrue(is_valid_row_or_col('5'))
        self.assertTrue(is_valid_row_or_col('1'))
        self.assertTrue(is_valid_row_or_col('10'))

    def test_row_or_col_validator_invalid_count(self):
        """ Valid tickets are between 1 and 10"""
        self.assertFalse(is_valid_row_or_col('11'))
        self.assertFalse(is_valid_row_or_col('0'))
        self.assertFalse(is_valid_row_or_col('-1'))
        self.assertFalse(is_valid_row_or_col('1434019341049132'))

    def test_row_or_col_validator_invalid_number(self):
        self.assertFalse(is_valid_row_or_col('1.212'))
        self.assertFalse(is_valid_row_or_col('1.21e2'))
        self.assertFalse(is_valid_row_or_col('The Real is on the Rise'))
        self.assertFalse(is_valid_row_or_col(''))
        self.assertFalse(is_valid_row_or_col('\n\t\r'))
        self.assertFalse(is_valid_row_or_col(None))

if __name__ == '__main__':
    unittest.main()
