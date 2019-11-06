from pypika import Query, Table, Schema, Criterion
from pypika.queries import QueryBuilder
import asyncio
import typing
import asyncpg
from loguru import logger
#import dsnparse
from utils import ConnGen
from meta_model import Model
from my_query_builder import MyQueryBuilder, T
from fields.simple_fields import FieldInt, FieldStr, OneToOneField
from utils import get_all_property

class DBType:
    UNKNOWN = 0
    PG = 1

class SimpleOrm:
    _schema: Schema
    _connection_string: str
    _connection_dict: dict
    _conn: asyncpg.Connection
    _db_type: DBType

    def __init__(self, schema_name: str = None,):
        self._schema = Schema(schema_name) if schema_name != None else None
        self._repository = {}

    def entity(self, model: typing.Type[Model],):
        model._table = Table(model.__table__, schema=self._schema)
        model._orm = self
        model.find = MyQueryBuilder[model](self, model).from_(model._table).select
        model._include = MyQueryBuilder[model](self, model).from_(model._table).join
        model._query = MyQueryBuilder[model](self, model).from_(model._table)
        
        model._fields = []
        self._repository[model.__name__] = model
        for i in get_all_property(model.__dict__['__annotations__'], model.__dict__):
            model.__dict__[i]._setup(i)
            model.__dict__[i]._orm = self
            #logger.info(model.__dict__[i].name)
            model._fields.append(model.__dict__[i])
        
        #a = model._query.select(*[i for i in model._fields if i._required == True])
        #print(a)

    @property
    def connection_string(self):
        return self._connection_string
    

    @connection_string.setter
    def connection_string(self, value: typing.Union[str, dict],):
        if isinstance(value, str):
            self._connection_string = value
            #TODO: implement parsing connection string
        elif isinstance(value, dict):
            self._connection_dict = value


    async def connect(self,):
        self._conn = await asyncpg.connect(**self._connection_dict)