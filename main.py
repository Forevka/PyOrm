import asyncio
from simple_orm import SimpleOrm
from models import User, Address, Question

from loguru import logger

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
  orm.entity(Question)

  print(User.get_pk())

  user = User.filter().include(User.address).query
  print(user)
  u = await user.all()
  print(u)

  ''' users = await User.filter().all()
  for i in users:
      print(i)
  
  addresses = await Address.filter().all()
  for i in addresses:
      print(i)'''

if __name__ == "__main__":
    asyncio.run(main())