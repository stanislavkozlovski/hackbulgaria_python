import json
from validate_email import validate_email
from datetime import datetime

VALID_JSON_OBJECTS = {list, dict, set, str, int, float, bool, None}


class serializer(type):
    def __new__(cls, name, bases, clsdict):

        wanted_fields = {}
        for attr, value in clsdict.items():
            if not callable(value) and not (attr.startswith('__') and attr.endswith('__')):
                wanted_fields[attr] = value

        # remove the fields from the dict
        for attr, _ in wanted_fields.items():
            del clsdict[attr]

        clsdict['_wanted_fields'] = wanted_fields
        clsobj = super().__new__(cls, name, bases, clsdict)
        return clsobj


class Serializer(metaclass=serializer):
    """
    A serializer where we store all our wanted variables in a dictionary _wanted_fields.
    Upon creation, an instance of a class is passed which should have all our wanted variables in it.
    We check for that and attach each variable is does have to the key of our _wanted_fields
    """
    def __init__(self, instance):
        self.instance = instance
        self._is_valid = True
        # check if it's valid and attach all the valid data to its corresponding key in self._wanted_fields
        self.update_fields()

        if self._is_valid:
            self.data = self.create_data()

    def update_fields(self):
        for attr, val in vars(self.instance).items():
            if attr not in self._wanted_fields and not self._wanted_fields[attr].validate_value(val):
                self._is_valid = False
            else:
                self._wanted_fields[attr].value = val

    def create_data(self):
        return json.dumps({k:val.convert_value_to_json() for k, val in self._wanted_fields.items()}
                          , indent=4)

    def is_valid(self):
        return self._is_valid


class Comment(object):
    def __init__(self, email, content, created_at=None):
        self.email = email
        self.content = content

        if created_at is None:
            created_at = datetime.now()

        self.created_at = created_at


class FieldMixin:
    def convert_value_to_json(self):
        if self.value.__class__ in VALID_JSON_OBJECTS:
                return self.value
        return str(self.value)


class Email(FieldMixin):
    def validate_value(self, value):
        return validate_email(self.value)


class Char(FieldMixin):
    def validate_value(self, value):
        return isinstance(value, str)


class DateTime(FieldMixin):
    def validate_value(self, value):
        return isinstance(value, datetime)


class CommentSerializer(Serializer):
    email = Email()
    content = Char()
    created_at = DateTime()


comment = Comment(email='radorado@hakbulgaria.com', content='wie naistina li hakvate?')
srlzr = CommentSerializer(comment)
print(srlzr.is_valid())
print(srlzr.data)
"""
{
  "email": "radorado@hackbulgaria.com",
  "content": "wie naistina li hakvate?",
  "created_at": "'2017-01-20T13:43:10.704846'"
}
"""