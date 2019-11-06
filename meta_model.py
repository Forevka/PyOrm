from fields.simple_fields import OneToOneField
from pypika import Query, Criterion, Field, Table
import typing
from loguru import logger
from my_query_builder import MyQueryBuilder
from utils import ConnGen, T, classproperty



class Model():
    __table__: str
    find: Query
    _conn: typing.Generic[ConnGen]
    _orm: None
    _table: Table
    _include: None
    _fields: typing.List[Field]
    _query: None

    _where_list = []
    _join_list = []

    @classproperty
    def query(cls):
      q = cls._query.select(
        *[cls._table[j.name].as_(cls.__name__+"_"+j.name) for j in cls._fields if j._required == True]
      ).where(
        Criterion.all(
          cls._where_list
        )
      )
      cls._query = MyQueryBuilder[cls](cls._orm, cls).from_(cls._table)
      return q


    @classmethod
    def filter(cls, *args) -> MyQueryBuilder[T]:
        logger.info(args[0].replace_table(None, cls._table))
        if args:
          cls._where_list.extend(
            [i.replace_table(None, cls._table) for i in args]
          )
        logger.info(cls._where_list)
        return cls
    
    @classmethod
    def include(cls, *args) -> MyQueryBuilder[T]:
        #logger.info(cls.__dict__)
        logger.info(cls._query)
        logger.info(cls._orm._repository[args[0].related_model]._table)
        logger.info(args)

        for entity in args:
          cls._query = cls._query.join(
            cls._orm._repository[entity.related_model]._table
          ).on(
            cls._orm._repository[entity.related_model]._table[entity.from_link] == cls._table[entity.to_link]
          ).select(*[cls._orm._repository[entity.related_model]._table[i.name].as_('orm_'+cls.__name__+"_"+cls._orm._repository[entity.related_model].__name__ + "_" + i.name) for i in cls._orm._repository[entity.related_model]._fields if i._required == True])
        
          logger.info(cls._query)
          
        return cls


    def marshall(self, *args, **kwargs):
        logger.info(kwargs)
        my_vals = {name.replace(self.__class__.__name__+"_", ''): field for name, field in kwargs.items() if name.startswith(self.__class__.__name__)}
        related_vals = {name.replace("orm_", ''): field for name, field in kwargs.items() if name.startswith("orm_")}
        logger.info(related_vals)
        logger.info(my_vals)
        for field in self._fields:
            #logger.info(field)
            if isinstance(field, OneToOneField):
                self.__dict__[field.name] = field._marshall({name.replace(self.__class__.__name__+"_"+field.related_model+"_", ""): val for name, val in related_vals.items() if name.startswith(self.__class__.__name__+"_"+field.related_model)})
            else:
                self.__dict__[field.name] = field._marshall(my_vals[field.name])
        
        logger.info(self.__dict__)
        return self
    
    def __str__(self) -> str:
        return f'{self.__class__.__name__} {", ".join([str(field.value) for name, field in self.__dict__.items()])}'