import json
import xml.etree.ElementTree as ET


class JsonableMixin:
    def to_json(self, indent=4):
        #  Create a dictionary of dictionaries
        json_info = {}
        json_info['dict'] = self.__dict__
        json_info['class_name'] = self.__class__.__name__
        # convert it to JSON
        return json.dumps(json_info, indent=indent)

    @classmethod
    def from_json(cls, json_str):
        json_info = json.loads(json_str)
        kwargs = json_info['dict']
        wanted_class_name = json_info['class_name']

        if wanted_class_name != cls.__name__:
            raise ValueError(f"You can't create a {wanted_class_name} from a {cls.__name__}!")

        wanted_class = globals().get(wanted_class_name)
        return wanted_class(**kwargs)


class XmlableMixin:
    def to_xml(self):
        xml_info = ET.Element(self.__class__.__name__)
        xml_info.attrib = {}
        for k, v in self.__dict__.items():
            key = ET.SubElement(xml_info, str(k))
            key.text = str(v)

        return ET.tostring(xml_info).decode('utf-8')

    @classmethod
    def from_xml(cls, xml_string):
        element_tree = ET.fromstring(xml_string)
        if element_tree.tag != cls.__name__:
            raise ValueError(f"You can't create a {cls.__name__} Object from {element_tree.tag}!")

        # build the kwargs
        kwargs = {}
        for child in element_tree:
            kwargs[child.tag] = child.text

        return cls(**kwargs)


class Panda(JsonableMixin, XmlableMixin):
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name


class Person(JsonableMixin, XmlableMixin):
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name


