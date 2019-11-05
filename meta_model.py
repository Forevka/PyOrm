from pypika import Query, Criterion
import typing
from loguru import logger
from my_query_builder import MyQueryBuilder
from utils import ConnGen, T



class Model():
    __table__: str
    find: Query
    _conn: typing.Generic[ConnGen]
    _fields: typing.List[str]

    @classmethod
    def filter(cls, *args) -> MyQueryBuilder[T]:
        q = cls.find(*cls.__dict__['__annotations__']).where(
            Criterion.all([
                *args
            ])
        )
        return q
    
    def marshall(self, *args, **kwargs):
        logger.info(kwargs)
        for name, field in self.__class__.__annotations__.items():
            logger.info(field)
            self.__dict__[name] = field()._marshall(kwargs[name])
        
        logger.info(self.__dict__)
        return self
    
    def __str__(self) -> str:
        return f'{self.__class__.__name__} {", ".join([str(i.value) for i in self.__dict__.values()])}'