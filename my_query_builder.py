from utils import T
from pypika.queries import QueryBuilder
import asyncpg
import typing
from loguru import logger


class MyQueryBuilder(QueryBuilder, typing.Generic[T]):
    def __init__(self, orm, model: 'Model', *args, **kwargs):
        self.db: 'SimpleOrm' = orm
        self.model = model
        super(MyQueryBuilder, self).__init__(*args, **kwargs)

    async def first(self,) -> T:
        raw_model = await self.db._conn.fetchrow(self.get_sql())
        if raw_model:
            return self.model().marshall(**raw_model)
    
    async def all(self,) -> typing.List[T]:
        raw_models = await self.db._conn.fetch(self.get_sql())
        if raw_models:
            return [self.model().marshall(**raw_model) for raw_model in raw_models]
        return []
    
    def include(self, *args):
        print(type(self))
        print(self)
        for field in args:
            #print(entity)
            print(field.related_model)
            address = self.db._repository[field.related_model]._table
            self.join(
                address
            ).on(
                self.db._repository[field.related_model]._table.a == self.db._repository[field.related_model]._table.a
            )
            print(self)
        #self.join()
