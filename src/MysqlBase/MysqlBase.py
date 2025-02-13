import aiomysql
import os
from commond.commond import compareHash

class MysqlService: 
     Instance = None

     @classmethod
     async def init(self):
          try:
               if self.Instance is None:
                    self.Instance = await aiomysql.create_pool(
                         host=os.getenv('DB_HOST'),
                         user=os.getenv('DB_USER'),
                         port=int(os.getenv('DB_PORT')),
                         password=os.getenv('DB_PASS'),
                         db=os.getenv('DB_NAME')
                    )
                    # self.cursor = self.Instance.cursor(dictionary=True)
                    print('Mysql service init')
          except Exception as err:
               raise Exception(f'Failed to initial mysql service: {err}')
          
     @classmethod
     async def exec(cls, sp: str, data: any = None): 
          cls.checkMysqlInitial()
          
          async with cls.Instance.acquire() as conn:
               async with conn.cursor(aiomysql.DictCursor) as cursor:
                    query = f"CALL {sp}({', '.join(['%s'] * len(data))})" if data else f"CALL {sp}()"
                    await cursor.execute(query, data or ())
                    return await cursor.fetchall()
     
     @classmethod
     async def login(cls, data):
          res = await cls.exec('sp_admin_login', [data.username])
          return { 'validate': compareHash(data.password, res[0]["password"]), 'id': res[0]['id']}

     @classmethod
     async def updateAdminLoginTime(cls, username: str):
          return await cls.exec('sp_update_admin_last_login', [username])
           

     @classmethod
     async def getProducts(cls):
          return await cls.exec('sp_get_all_product', [])

     @classmethod
     def checkMysqlInitial(cls):
          if cls.Instance is None:
               raise Exception(f'Mysql service is not initial')