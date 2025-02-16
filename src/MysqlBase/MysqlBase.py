import asyncio
from typing import List
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
                         db=os.getenv('DB_NAME'),
                         autocommit=True,
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

                    await conn.commit()
                    return await cursor.fetchall()
     
     @classmethod
     async def login(cls, data):
          cls.checkMysqlInitial()

          res = await cls.exec('sp_admin_login', [data.username])
          return { 'validate': compareHash(data.password, res[0]["password"]), 'id': res[0]['id']}

     @classmethod
     async def updateAdminLoginTime(cls, username: str):
          cls.checkMysqlInitial()
          return await cls.exec('sp_update_admin_last_login', [username])
           

     @classmethod
     async def getProducts(cls):
          cls.checkMysqlInitial()
          return await cls.exec('sp_get_all_product', [])

     @classmethod
     async def updateProductDescribe(cls, productId: int, describe: str):
          cls.checkMysqlInitial()
          return await cls.exec('sp_update_product_describe', [productId, describe])
     
     @classmethod
     async def updateProductDetail(cls, productId: int, productName: str, parentId: int, icon: str):
          cls.checkMysqlInitial()
          return await cls.exec('sp_update_product_detail', [productId, productName, parentId, icon])

     @classmethod
     async def updateProductStatus(cls, productId: List[int], status: int):
          cls.checkMysqlInitial()
          await asyncio.gather(*[cls.exec('sp_update_product_status', [x, status]) for x in productId])
          return 
     
     @classmethod
     async def deleteProduct(cls, productId: int):
          cls.checkMysqlInitial()
          await asyncio.gather(*[cls.exec('sp_delete_product', [x]) for x in productId]) 
          return 
     
     @classmethod
     async def addProduct(cls, productName: str, parentId: str, icon: str, describe: List[str]):
          cls.checkMysqlInitial()
          return await cls.exec('sp_add_product', [productName, parentId, icon, describe])

     @classmethod
     async def updateProductParentId(cls, originalId: int, newId: int):
          cls.checkMysqlInitial()
          return await cls.exec('sp_update_prodcut_parent_id', [originalId, newId])
     
     @classmethod
     async def getItems(cls):
          cls.checkMysqlInitial()
          return await cls.exec('sp_get_all_item', [])
     
     @classmethod
     async def updateItemDetail(cls, id: int, itemName: str, parentId: str, price: float, qty: int, img: str):
          cls.checkMysqlInitial()
          return await cls.exec('sp_update_item_detail', [id, itemName, parentId, price, qty, img])
     
     @classmethod
     async def updateItemDescribe(cls, id: int, describe: str):
          cls.checkMysqlInitial()
          return await cls.exec('sp_update_item_describe', [id, describe])

     @classmethod
     async def updateItemStatus(cls, itemId: List[int], status: int):
          cls.checkMysqlInitial()
          await asyncio.gather(*[cls.exec('sp_update_item_status', [x, status]) for x in itemId])
          return 

     @classmethod
     async def deleteItem(cls, itemId: List[int]):
          cls.checkMysqlInitial()
          await asyncio.gather(*[cls.exec('sp_delete_item', [x]) for x in itemId]) 
          return 
     
     @classmethod
     async def updateItemParentId(cls, originalId: int, newId: int):
          cls.checkMysqlInitial()
          return await cls.exec('sp_update_item_parent_id', [originalId, newId])
     
     @classmethod
     async def addItem(cls, itemName: str, parentId: int, quantity: int, price: int, image: str ,describe: str):
          cls.checkMysqlInitial()
          return await cls.exec('sp_add_item', [itemName, parentId, quantity, price, image, describe])

     @classmethod
     def checkMysqlInitial(cls):
          if cls.Instance is None:
               raise Exception(f'Mysql service is not initial')