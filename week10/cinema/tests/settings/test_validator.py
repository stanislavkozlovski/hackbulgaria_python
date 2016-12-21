import unittest
from settings.validator import is_valid_spell


class ValidatorTests(unittest.TestCase):
    def test_is_valid_spell_valid_spell(self):
        self.assertTrue(is_valid_spell("show movies"))

    def test_is_valid_spell_invalid_spell(self):
        self.assertFalse(is_valid_spell("show kookies"))

    def test_is_valid_spell_int(self):
        self.assertFalse(is_valid_spell(5))

if __name__ == '__main__':
    unittest.main()