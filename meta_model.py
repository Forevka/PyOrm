from fields.simple_fields import OneToManyField
from pypika import Query, Criterion, Field, Table, JoinType
import typing
from loguru import logger
from my_query_builder import MyQueryBuilder
from utils import ConnGen, T, classproperty, get_all_property



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

    _temp_data = []
    _related = []

    def __init__(self):
      self._related = []
      self._fields = []

    @classproperty
    def query(cls):
      q = cls._query.select(
        *[cls._table[j.name].as_(cls.__name__+"_"+j.name) for j in cls._fields if j._required == True]
      ).where(
        Criterion.all(
          [i.replace_table(None, cls._table) for i in cls._where_list]
        )
      )
      cls._query = MyQueryBuilder[cls](cls._orm, cls).from_(cls._table)
      return q


    @classmethod
    def filter(cls, *args) -> MyQueryBuilder[T]:
        #logger.info(args[0].replace_table(None, cls._table))
        if args:
          cls._where_list.extend(
            args
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
            cls._orm._repository[entity.related_model]._table, JoinType.left
          ).on(
            cls._orm._repository[entity.related_model]._table[entity.to_link] == cls._table[entity.from_link]
          ).select(*[cls._orm._repository[entity.related_model]._table[i.name].as_('orm_'+cls.__name__+"_"+cls._orm._repository[entity.related_model].__name__ + "_" + i.name) for i in cls._orm._repository[entity.related_model]._fields if i._required == True])
        
          logger.info(cls._query)
          
        return cls

    def add_related_data(self, data):
      logger.info(self)
      logger.info(data)
      self._related.append(data)

    def marshall_related(self):
      logger.info(self)
      logger.info(self._related)

    def marshall(self, vals):
        '''logger.info(raw_records)
        dbo = []
        for record in raw_records:
          print(record)
          m = self._orm._repository[self.__class__.__name__]()
          model_name = self.__class__.__name__ + "_"
          temp_name = 'orm_' + model_name
          
          temp = {name:val for name, val in record.items() if not name.startswith(self.__class__.__name__)}
          model_data = {name.replace(model_name, ''):val for name, val in dict(record).items() - temp.items()}
          temp = {name.replace(temp_name, ''):val for name, val in temp.items()}
          logger.info(model_data)
          logger.info(temp)
          dbo.append()'''
        '''my_vals = {name.replace(self.__class__.__name__+"_", ''): field for name, field in kwargs.items() if name.startswith(self.__class__.__name__)}
        related_vals = {name.replace("orm_", ''): field for name, field in kwargs.items() if name.startswith("orm_")}
        logger.info(related_vals)
        logger.info(my_vals)'''
        logger.info(list(get_all_property(self.__class__.__dict__['__annotations__'], self.__dict__)))
        for field in self._fields:
            #logger.info(field)
            if isinstance(field, OneToManyField):
              pass
              #self.__dict__[field.name] = field._marshall(vals[field.name])
            else:
              self.__dict__[field.name] = field.__class__()._marshall(vals[field.name])
        
        logger.info(self.__dict__)
        #return self
    
    @classmethod
    def instance(cls,):
      logger.info(cls)
      return cls()

    @classmethod
    def get_pk(cls,):
      return [i for i in cls._fields if i.primary_key]

    def __str__(self) -> str:
        logger.info([field for field in self._fields])
        return f'{self.__class__.__name__} {", ".join([field for field in self._fields])}'
    
    def __repr__(self):
      return str(self)
    
    def __hash__(self,):
      my_pk_vals = [self.__dict__[i.name].value for i in self.__class__.get_pk()]
      logger.info(my_pk_vals)
      return hash((*my_pk_vals, self.__class__))