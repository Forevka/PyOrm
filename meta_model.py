from fields.simple_fields import OneToOneField
from pypika import Query, Criterion, Field, Table
import typing
from loguru import logger
from my_query_builder import MyQueryBuilder
from utils import ConnGen, T



class Model():
    __table__: str
    find: Query
    _conn: typing.Generic[ConnGen]
    _table: Table
    _include: None
    _fields: typing.List[Field]

    @classmethod
    def filter(cls, *args) -> MyQueryBuilder[T]:
        #logger.info(cls.)
        q = cls.find(*[i for i in cls._fields if i._required == True]).where(
            Criterion.all([
                *args
            ])
        )

        return q
    
    @classmethod
    def include(cls, *args) -> MyQueryBuilder[T]:
        logger.info(cls)
        logger.info(args)
        q = cls._include(
            args[0].related_model
        ).on(
            'a' == 'a'
        )

        return q


    def marshall(self, *args, **kwargs):
        logger.info(kwargs)
        for name, field in self.__class__.__annotations__.items():
            logger.info(field)
            if issubclass(field, OneToOneField):
                pass
            else:
                self.__dict__[name] = field()._marshall(kwargs[name])
        
        logger.info(self.__dict__)
        return self
    
    def __str__(self) -> str:
        return f'{self.__class__.__name__} {", ".join([str(field.value) for name, field in self.__dict__.items()])}'