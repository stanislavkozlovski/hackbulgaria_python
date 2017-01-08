import unittest
from settings.validator import is_valid_spell, is_valid_date


class ValidatorTests(unittest.TestCase):
    def test_is_valid_spell_valid_spell(self):
        self.assertTrue(is_valid_spell("show movies"))

    def test_is_valid_spell_invalid_spell(self):
        self.assertFalse(is_valid_spell("show kookies"))

    def test_is_valid_spell_int(self):
        self.assertFalse(is_valid_spell(5))

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

if __name__ == '__main__':
    unittest.main()
