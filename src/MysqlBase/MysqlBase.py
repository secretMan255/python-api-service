import asyncio
from typing import List
import aiomysql
import os
from commond.commond import compareHash
import json

class MysqlService: 
     Instance = None
     loop = None

     @classmethod
     async def init(cls):
          try:
               if cls.Instance is None:
                    unix_socket_path = f"/cloudsql/{os.getenv('INSTANCE_CONNECTION_NAME')}"
                    cls.Instance = await aiomysql.create_pool(
                         host=os.getenv('DB_HOST'),
                         user=os.getenv('DB_USER'),
                         port=int(os.getenv('DB_PORT')),
                         password=os.getenv('DB_PASS'),
                         db=os.getenv('DB_NAME'),
                         # unix_socket=unix_socket_path,
                         autocommit=True,
                         loop=cls.loop,
                    )
                    # self.cursor = self.Instance.cursor(dictionary=True)
                    print('Mysql service init')
          except Exception as err:
               raise Exception(f'Failed to initial mysql service: {err}')
          
     @classmethod
     async def exec(cls, sp: str, data: any = None): 
          try:
               cls.checkMysqlInitial()
               
               async with cls.Instance.acquire() as conn:
                    async with conn.cursor(aiomysql.DictCursor) as cursor:
                         query = f"CALL {sp}({', '.join(['%s'] * len(data))})" if data else f"CALL {sp}()"
                         await cursor.execute(query, data or ())

                         await conn.commit()
                         return await cursor.fetchall()
          except aiomysql.Error as e:
               print(f"MySQL error: {e}, reconnecting...")
               await cls.init() 
               return await cls.exec(sp, data)
     
     @classmethod
     async def login(cls, data):
          cls.checkMysqlInitial()
          print('login data: ', data)
          res = await cls.exec('sp_admin_login', [data.username])
          print('res: ' , res)
          if not res:
               return { 'validate' : False }
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
          return await asyncio.gather(*[cls.exec('sp_delete_product', [x]) for x in productId]) 
     
     @classmethod
     async def addProduct(cls, productName: str, parentId: str, icon: str, describe: str):
          cls.checkMysqlInitial()
          describe_value = describe
          if isinstance(describe_value, (list, dict)):
               describe_value = json.dumps(describe_value)
               
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
     async def deleteItemByPId(cls, itemId: List[int]):
          cls.checkMysqlInitial()
          print('p_id: ' , itemId)
          await asyncio.gather(*[cls.exec('sp_delete_item_by_p_id', [x]) for x in itemId])
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
     async def getCarousel(cls):
          cls.checkMysqlInitial()
          return await cls.exec('sp_get_carousel')
     
     @classmethod
     async def updateCarousel(cls, id: int, name: str, parentId: int):
          cls.checkMysqlInitial()
          return await cls.exec('sp_update_carousel', [id, name, parentId])
     
     @classmethod
     async def addCarousel(cls, name: str, parentId: int):
          cls.checkMysqlInitial()
          return await cls.exec('sp_add_carousel' , [name, parentId])
     
     @classmethod
     async def deleteCarousel(cls, id: List[int]):
          cls.checkMysqlInitial()
          await asyncio.gather(*[cls.exec('sp_delete_carousel', [x]) for x in id]) 
          return 
     
     @classmethod
     async def deleteCarouselById(cls, id: List[int]):
          cls.checkMysqlInitial()
          await asyncio.gather(*[cls.exec('sp_delete_carousel_by_p_id', [x]) for x in id]) 
          return 

     @classmethod
     async def updateCarouselParentId(cls, originId: int , newId: int):
          cls.checkMysqlInitial()
          return await cls.exec('sp_update_carousel_parent_id', [originId, newId])

     @classmethod
     async def getMainProduct(cls):
          cls.checkMysqlInitial()
          async with cls.Instance.acquire() as conn:
               async with conn.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute("CALL sp_get_main_product()")
                    
                    # Fetch first result set (Main Products)
                    main_products = await cursor.fetchall()
                    
                    # Move to the second result set (Available Products)
                    await cursor.nextset()
                    available_products = await cursor.fetchall()
          return {
               "mainProducts": main_products,
               "availableProducts": available_products
          }
     
     @classmethod
     async def deleteMainProduct(cls, id: List[int]):
          cls.checkMysqlInitial()
          await asyncio.gather(*[cls.exec('sp_delete_main_product', [x]) for x in id]) 
          return
     
     @classmethod
     async def deleteMainProductById(cls, id: List[int]):
          cls.checkMysqlInitial()
          await asyncio.gather(*[cls.exec('sp_delete_main_product_by_p_id', [x]) for x in id]) 
          return
     
     @classmethod
     async def addMainProduct(cls, id: int):
          cls.checkMysqlInitial()
          return await cls.exec('sp_add_main_product', [id])
     
     @classmethod
     async def close(cls):
          if cls.Instance is not None:
               cls.Instance.close()
               await cls.Instance.wait_closed()
               cls.Instance = None
               print("MySQL service closed.")


     @classmethod
     def checkMysqlInitial(cls):
          if cls.Instance is None:
               raise Exception(f'Mysql service is not initial')