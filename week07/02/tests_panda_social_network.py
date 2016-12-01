import unittest
from panda_social_network import Panda, InvalidEmailError, PandaAlreadyThereError, PandasAlreadyFriendsError, SocialNetwork

class PandaTests(unittest.TestCase):
    def setUp(self):
        self.ivo = Panda('Ivo', 'bachvarov@gmail.com', 'male')
        self.ivo_copy = Panda('Ivo', 'bachvarov@gmail.com', 'male')
        self.roza = Panda('Rositsa', 'nqkoqsi@gmail.com', 'female')
        self.smith = Panda('John', 'smith@gmail.com', 'male')
        self.smalling = Panda('Paul', 'smalling@gmail.com', 'male')
        self.patrice = Panda('Evra', 'manchevr@gmail.com', 'male')
        self.girl = Panda('Girl', 'girl@gmail.com', 'female')

    def test_equal(self):
        self.assertNotEqual(self.ivo, self.roza)
        self.assertEqual(self.ivo, self.ivo_copy)

    def test_gender(self):
        self.assertTrue(self.girl.is_female())
        self.assertTrue(self.patrice.is_male())

    def test_invalid_email(self):
        with self.assertRaises(InvalidEmailError):
            Panda('Ivo', 'nqkoisi@.com', 'male')
            Panda('Ivo', 'nqkoisi@d.com', 'male')
            Panda('Ivo', 'nqkoisiBre.com', 'male')
            Panda('Ivo', 'nqkoisiBre@Abv.', 'male')
            Panda('Ivo', 'nqkoisiBre@Abv', 'male')

    def test_hash(self):
        """ Create three almost equal pandas and see if their hash function works
            as expected"""
        one = Panda('Ivo', 'ivo@gmail.com', 'male')
        two = Panda('Ivo', 'ivo@gmaiL.com', 'male')
        three = Panda('ivo', 'ivo@gmaiL.com', 'male')
        four = Panda('shopa', 'ivo@gmaiL.com', 'male')
        # create a set and see if all four pandas are there, if not, some have been overwritten
        pandas = {one, two, three, four}
        self.assertEqual(len(pandas), 4)
        # create a set again
        one_copy = Panda('Ivo', 'ivo@gmail.com', 'male')
        pandas = {one, one_copy}  # THESE SHOULD OVERWRITE
        self.assertNotEqual(len(pandas), 2)
        self.assertEqual(len(pandas), 1)

if __name__ == '__main__':
    unittest.main()