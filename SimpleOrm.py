from pypika import Query, Table, Schema, Criterion
from pypika.queries import QueryBuilder
import asyncio
import typing
import asyncpg
from loguru import logger
import dsnparse
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
        model.find = MyQueryBuilder[model](self, model).from_(model._table).select
        model._include = MyQueryBuilder[model](self, model).from_(model._table).join
        
        model._fields = []
        self._repository[model.__name__] = model
        for i in get_all_property(model.__dict__['__annotations__'], model.__dict__):
            model.__dict__[i]._setup(i)
            model._fields.append(model.__dict__[i])

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


class User(Model):
    __table__ = 'user'

    id: FieldInt = FieldInt(pk = True)
    name: FieldStr = FieldStr()
    age: FieldInt = FieldInt()

    address: OneToOneField = OneToOneField(related_model='Address', from_link='User.id', to_link='Address.id')


class Address(Model):
    __table__ = 'address'

    id: FieldInt = FieldInt(pk = True)
    descr: FieldStr = FieldStr()


async def main():
    db = {
        "user": "postgres",
        "password": "werdwerd2012",
        "database": "orm_test",
        "host": "194.67.198.163",
    }

    orm = SimpleOrm()
    orm.connection_string = db
    await orm.connect()

    orm.entity(User)
    orm.entity(Address)

    user =  User.include(User.address)
    print(user)

    users = await User.filter().all()
    for i in users:
        print(i)
    
    addresses = await Address.filter().all()
    for i in addresses:
        print(i)

if __name__ == "__main__":
    asyncio.run(main())