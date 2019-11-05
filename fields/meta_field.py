from pypika import Field
import typing

T = typing.TypeVar('T')


class MetaField(Field):
    name: str
    value: typing.Generic[T]
    _required: bool
    primary_key: bool

    def __init__(self, *args, required: bool = True, pk: bool = False):
        self._required = required
        self.primary_key = pk
        super(Field, self).__init__(self, *args)

    def _setup(self, varname: str):
        self.name = varname

    def _marshall(self, value: str):
        self.value = value
        return self
        
    def __str__(self,):
        return self.value
