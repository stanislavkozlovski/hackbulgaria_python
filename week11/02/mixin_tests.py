import unittest
from mixins import Panda, Person


class MixinsTest(unittest.TestCase):
    def setUp(self):
        self.panda_name = 'AaA'
        self.test_panda = Panda(name=self.panda_name)
        self.test_person = Person(name=self.panda_name)

    def test_to_json(self):
        expected_value = """{
    "dict": {
        "name": "AaA"
    },
    "class_name": "Panda"
}"""
        result = self.test_panda.to_json(indent=4)
        self.assertEqual(expected_value, result)

    def test_to_xml(self):
        expected_value = f"<Panda><name>{self.panda_name}</name></Panda>"
        result = self.test_panda.to_xml()
        self.assertCountEqual(expected_value, result)

    def test_to_json_from_json(self):
        """ Convert the panda object to a json and create a new panda object from that json"""
        json_panda = self.test_panda.to_json()
        new_panda = self.test_panda.from_json(json_panda)
        self.assertEqual(self.test_panda, new_panda)

    def test_to_xml_from_xml(self):
        """ Conver the Panda object to an XML and create the new Panda object from that XML"""
        xml_panda = self.test_panda.to_xml()
        new_panda = self.test_panda.from_xml(xml_panda)
        self.assertEqual(self.test_panda, new_panda)

    def test_panda_to_xml_from_person_xml(self):
        """ Try to create a Panda object from a Person XML"""
        xml_person = self.test_person.to_xml()
        with self.assertRaises(ValueError):
            self.test_panda.from_xml(xml_person)

    def test_panda_to_json_from_person_json(self):
        """ Try to create a Panda object from a Person JSON """
        json_person = self.test_person.to_json()
        with self.assertRaises(ValueError):
            self.test_panda.from_json(json_person)


if __name__ == '__main__':
    unittest.main()