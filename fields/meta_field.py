from pypika import Field
import typing
from loguru import logger

T = typing.TypeVar('T')


class MetaField(Field):
    name: str
    value: typing.Generic[T]
    _required: bool = True
    primary_key: bool

    def __init__(self, *args, required: bool = True, pk: bool = False):
        self._required = required
        self.primary_key = pk
        self.value = None
        super(Field, self).__init__(self, *args)

    def _setup(self, varname: str):
        self.name = varname

    def _marshall(self, value: str):
        logger.info(value)
        self.value = value
        return self
        
    def __str__(self,):
        return self.value
