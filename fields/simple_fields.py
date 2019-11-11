from .meta_field import MetaField, T
from pypika import Field
import typing

class FieldStr(MetaField):
  pass


class FieldInt(MetaField):
  pass


class OneToManyField(Field):
    name: str
    value: typing.Generic[T]
    from_link: str
    to_link: str
    related_model: 'Model'
    primary_key = False
    _required: bool = False
    _orm: None

    def __init__(self, *args, related_model = None, from_link = '', to_link = '',):
        self.from_link = from_link
        self.value = None
        self.to_link = to_link
        self.related_model = related_model
        self._required = False
        super(Field, self).__init__(self, *args)

    def _setup(self, varname: str):
        self.name = varname

    def _marshall(self, values: dict):
        print(values)
        self.value = values
        return self
        
    def __str__(self,):
        return str(self.value)