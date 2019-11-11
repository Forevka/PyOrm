from utils import T
from pypika.queries import QueryBuilder
import asyncpg
import typing
from loguru import logger


class MyQueryBuilder(QueryBuilder, typing.Generic[T]):
    def __init__(self, orm, model: 'Model', *args, **kwargs):
        self.db: 'SimpleOrm' = orm
        self.model = model
        self.dbos = {}
        super(MyQueryBuilder, self).__init__(*args, **kwargs)

    async def first(self,) -> T:
        raw_model = await self.db._conn.fetchrow(self.get_sql())
        if raw_model:
            return self.model().marshall(**raw_model)
    
    async def all(self,) -> typing.List[T]:
        raw_records = await self.db._conn.fetch(self.get_sql())
        #logger.info(raw_models)
        logger.info(raw_records)
        dbo = []
        
        for record in raw_records:
          #m = self.model._orm._repository[self.model.__name__]()
          model_name = self.model.__name__ + "_"
          temp_name = 'orm_' + model_name
          
          temp = {name:val for name, val in record.items() if not name.startswith(self.model.__name__)}
          model_data = {name.replace(model_name, ''): val for name, val in dict(record).items() - temp.items()}
          m = self.add_if_no_exists_else_exists(model_data, self.model)
          logger.info(m)
          logger.info(self.dbos)
          temp = {name.replace(temp_name, ''):val for name, val in temp.items()}
          logger.info(temp)
          m.add_related_data(temp)

          for i in self.dbos.values():
            logger.info(i._related)
        
        for i in self.dbos.values():
          i.marshall_related()

        return []

    def add_if_no_exists_else_exists(self, data, model_type):
      a = model_type() == model_type()
      logger.info(a)
      model = model_type()
      logger.info(id(model))
      model.marshall(data)
      #u.id._marshall(data['id'])
      u_hash = hash(model)
      logger.info(u_hash)
      if u_hash in self.dbos.keys():
        pass
      else:
        self.dbos[u_hash] = model
      return self.dbos[u_hash]
        

