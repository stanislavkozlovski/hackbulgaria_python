import unittest
from panda_social_network import Panda, PandaSocialNetwork
from custom_exceptions import InvalidEmailError, PandaAlreadyThereError, PandasAlreadyFriendsError

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
        self.assertTrue(self.girl.isFemale())
        self.assertTrue(self.patrice.isMale())

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


class SocialNetworkTests(unittest.TestCase):
    def setUp(self):
        self.ivo = Panda('Ivo', 'bachvarov@gmail.com', 'male')
        self.ivo_copy = Panda('Ivo', 'bachvarov@gmail.com', 'male')
        self.roza = Panda('Rositsa', 'nqkoqsi@gmail.com', 'female')
        self.smith = Panda('John', 'smith@gmail.com', 'male')
        self.smalling = Panda('Paul', 'smalling@gmail.com', 'male')
        self.patrice = Panda('Evra', 'manchevr@gmail.com', 'male')
        self.girl = Panda('Girl', 'girl@gmail.com', 'female')
        self.friendless_guy = Panda('Friendless', 'guy@gmail.com', 'male')

        self.social_network = PandaSocialNetwork()
        self.social_network.add_panda(self.friendless_guy)
        self.social_network.make_friends(self.ivo, self.roza)
        self.social_network.make_friends(self.ivo, self.smith)
        self.social_network.make_friends(self.ivo, self.smalling)
        self.social_network.make_friends(self.patrice, self.smalling)
        self.social_network.make_friends(self.patrice, self.girl)


    def test_add_panda(self):
        social_network = PandaSocialNetwork()
        social_network.add_panda(self.ivo)
        social_network.add_panda(self.roza)
        self.assertEqual(social_network.pandas, [self.ivo, self.roza])

    def test_has_panda(self):
        social_network = PandaSocialNetwork()
        social_network.add_panda(self.ivo)
        self.assertTrue(social_network.has_panda(self.ivo))

    def test_add_panda_already_there(self):
        """ Add a panda that's already in the social network """
        social_network = PandaSocialNetwork()
        social_network.add_panda(self.ivo)
        with self.assertRaises(PandaAlreadyThereError):
            social_network.add_panda(self.ivo)

    def test_make_friends(self):
        """ Make two pandas friends, then try to make them friends again"""
        social_network = PandaSocialNetwork()
        # don't add them to the social network
        social_network.make_friends(self.ivo, self.roza)
        with self.assertRaises(PandasAlreadyFriendsError):
            social_network.make_friends(self.ivo, self.roza)

    def test_are_friends(self):
        social_network = PandaSocialNetwork()
        social_network.make_friends(self.ivo, self.smith)
        social_network.make_friends(self.ivo, self.roza)
        self.assertTrue(social_network.are_friends(self.ivo, self.roza))
        self.assertTrue(social_network.are_friends(self.ivo, self.smith))
        self.assertFalse(social_network.are_friends(self.roza, self.smith))

    def test_friends_of(self):
        self.assertFalse(self.social_network.friends_of(self.friendless_guy))
        self.assertEqual(
            self.social_network.friends_of(self.girl),
            [self.patrice]  # girl is friends with patrice only
        )

    def test_connection_level(self):
        self.assertEqual(self.social_network.connection_level(self.ivo, self.roza), 1)
        self.assertEqual(self.social_network.connection_level(self.ivo, self.girl), 3)
        self.assertEqual(self.social_network.connection_level(self.ivo, self.friendless_guy), -1)

    def test_are_connected(self):
        self.assertTrue(self.social_network.are_connected(self.ivo, self.girl))
        self.assertFalse(self.social_network.are_connected(self.ivo, self.friendless_guy))

    def test_how_many_genders(self):
        self.assertEqual(self.social_network.how_many_gender_in_network(1, self.friendless_guy, 'male'), 0)
        self.assertEqual(self.social_network.how_many_gender_in_network(1, self.girl, 'female'), 0)
        self.assertEqual(self.social_network.how_many_gender_in_network(4, self.girl, 'female'), 1)

    def test_save_load(self):
        file_name = 'saved.json'
        self.social_network.save(file_name)
        loaded_social_network = PandaSocialNetwork.load(file_name)
        # test the loaded social network
        self.assertEqual(loaded_social_network.how_many_gender_in_network(1, self.friendless_guy, 'male'), 0)
        self.assertEqual(loaded_social_network.how_many_gender_in_network(1, self.girl, 'female'), 0)
        self.assertEqual(loaded_social_network.how_many_gender_in_network(4, self.girl, 'female'), 1)
        self.assertTrue(loaded_social_network.are_connected(self.ivo, self.girl))
        self.assertFalse(loaded_social_network.are_connected(self.ivo, self.friendless_guy))
        self.assertEqual(loaded_social_network.connection_level(self.ivo, self.roza), 1)
        self.assertEqual(loaded_social_network.connection_level(self.ivo, self.girl), 3)
        self.assertEqual(loaded_social_network.connection_level(self.ivo, self.friendless_guy), -1)
        self.assertFalse(loaded_social_network.friends_of(self.friendless_guy))
        self.assertEqual(
            loaded_social_network.friends_of(self.girl),
            [self.patrice]  # girl is friends with patrice only
        )

if __name__ == '__main__':
    unittest.main()