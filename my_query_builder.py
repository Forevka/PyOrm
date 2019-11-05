from meta_model import Model, T
from pypika.queries import QueryBuilder
import asyncpg
import typing
from loguru import logger


class MyQueryBuilder(QueryBuilder):
    def __init__(self, db_connection, model: Model, *args, **kwargs):
        self.conn: asyncpg.Connection = db_connection
        self.model = model
        super(MyQueryBuilder, self).__init__(*args, **kwargs)

    async def first(self,) -> typing.Optional[T]:
        raw_model = await self.conn.fetchrow(self.get_sql())
        if raw_model:
            return self.model().marshall(**raw_model)
    
    async def all(self,) -> T:
        raw_models = await self.conn.fetch(self.get_sql())
        if raw_models:
            return [self.model().marshall(**raw_model) for raw_model in raw_models]
        return []
