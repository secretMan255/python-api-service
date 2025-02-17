from quart import jsonify, make_response
from ApiBase.ApiBase import ApiBase
from validateParam.pydantic import DeleteCarouselValidate, AddCarouselValidate, CarouselValidate, AddItemValidate, UpdateItemParentIdValidate, DeleteItemValidate, UpdateItemStatusValidate, UpdateItemDescribeValidate, UpdateItemDetailValidate, LoginValidate, UpdateProductDescribeValidate, UpdateProductDetailValidate, UpdateProductStatusValidate, DeleteProductValidate, AddProductValidate, UpdateProductParentIdValidate
from MysqlBase.MysqlBase import MysqlService

async def test(request):
     return 'test test'

async def onLogin(request):
     isValid, data = LoginValidate(request)
     
     if not isValid:
          return jsonify({"msg": f'Invalid input - {data}'})
     
     res = await MysqlService.login(data)
     
     if res.get('validate') is True:
          tokenInfor = {
               'id': res.get('id'),
               'username': data.username,
               'role': data.role
          }
          print('tokenInfor: ', tokenInfor)

          token = ApiBase.generateToken(tokenInfor)

          response = await make_response(jsonify(
               {
                    'ret': -1, 
                    'data': {
                         'status': 0,
                         'msg': 'Login successful'
                    }
               }
          ))
          response.set_cookie(
               'authToken',
               token,
               httponly=True,  # Prevent JavaScript access
               secure=False,  # HTTPS only
               samesite='Strict',  # Prevent CSRF
               max_age=3600,  # 1 hour expiration
               path='/'
          )

          await MysqlService.updateAdminLoginTime(data.username)
          return response
     else:
          return {  
               'status': -1,
               'msg': 'Invalid credential'
          }
     
async def onLogout(request):
     response = await make_response(jsonify(
                    {
                         'ret': -1, 
                         'data': {
                              'status': 0,
                              'msg': 'Logout successful'
                         }
                    }
               ))
     response.set_cookie(
          "authToken", 
          "", 
          httponly=True,  
          secure=False,   
          samesite="Strict", 
          max_age=0, 
          path="/"  
     )
     return response

async def onGetProducts(request):
     return await MysqlService.getProducts()

async def onUpdateProductDescribe(request):
     isValid, data = UpdateProductDescribeValidate(request)
     if not isValid:
          return jsonify({"status" : -1, "msg": f'Invalid input - {data}'})
     
     return await MysqlService.updateProductDescribe(data.productId, data.describe)

async def onUpdateProductDetail(request):
     isValid, data = UpdateProductDetailValidate(request)
     if not isValid:
          return jsonify({"status" : -1, "msg" : f'Invalid input - {data}'})

     return await MysqlService.updateProductDetail(data.productId, data.productName, data.parentId, data.icon)

async def onUpdateProductStatus(request):
     isValid, data = UpdateProductStatusValidate(request)
     if not isValid:
          return jsonify({'status': -1, 'msg': f'Invalid input - {data}'})

     return await MysqlService.updateProductStatus(data.productId, data.status)

async def onDeleteProduct(request):
     isValid, data = DeleteProductValidate(request)
     if not isValid:
          return jsonify({'status': -1, 'msg': f'Invalid input - {data}'})
     return await MysqlService.deleteProduct(data.productId)

async def onUpdateProductPerantId(request):
     isValid, data = UpdateProductParentIdValidate(request)
     if not isValid:
          return jsonify({'status': -1, 'msg': f'Invalid input - {data}'})
     return await MysqlService.updateProductParentId(data.originalParentId, data.newParentId)

async def onAddProduct(request):
     isValid, data = AddProductValidate(request)
     if not isValid:
          return jsonify({'status': -1, 'msg': f'Invalid input - {data}'})
     return await MysqlService.addProduct(data.productName, data.parentId, data.icon, data.describe)

async def onGetItems(request):
     return await MysqlService.getItems()

async def onUpdateItemDetail(request):
     isValid, data = UpdateItemDetailValidate(request)
     if not isValid:
          return jsonify({'status': -1, 'msg': f'Invalid input - {data}'})
     return await MysqlService.updateItemDetail(data.itemId, data.itemName, data.itemParentId, data.itemPrice, data.itemQty, data.itemImg)

async def onUpdateItemDescribe(request):
     isValid, data = UpdateItemDescribeValidate(request)
     if not isValid:
          return jsonify({'status': -1, 'msg': f'Invalid input - {data}'})
     return await MysqlService.updateItemDescribe(data.itemId, data.itemDescribe)

async def onUpdateItemStatus(request):
     isValid, data = UpdateItemStatusValidate(request)
     if not isValid:
          return jsonify({'status': -1, 'msg': f'Invalid input - {data}'})
     return await MysqlService.updateItemStatus(data.itemId, data.status)

async def onDeleteItem(request):
     isValid, data = DeleteItemValidate(request)
     if not isValid:
          return jsonify({'status': -1, 'msg': f'Invalid input - {data}'})
     return await MysqlService.deleteItem(data.itemId)

async def onUpdateItemParentId(request):
     isValid, data = UpdateItemParentIdValidate(request)
     if not isValid:
          return jsonify({'status': -1, 'msg': f'Invalid input - {data}'})
     return await MysqlService.updateItemParentId(data.originalParentId, data.newParentId)
     
async def onAddItem(request):
     isValid, data = AddItemValidate(request)
     if not isValid:
          return jsonify({'status': -1, 'msg': f'Invalid input - {data}'})
     return await MysqlService.addItem(data.itemName, data.parentId, data.quantity, data.price, data.image, data.describe)

async def onGetCarousel(request):
     return await MysqlService.getCarousel()

async def onUpdateCarousel(request):
     isValid, data = CarouselValidate(request)
     if not isValid:
          return jsonify({'status': -1, 'msg': f'Invalid input - {data}'})
     return await MysqlService.updateCarousel(data.id, data.name, data.parentId)

async def onAddCarousel(request):
     isValid, data = AddCarouselValidate(request)
     if not isValid:
          return jsonify({'status': -1, 'msg': f'Invalid input - {data}'})
     return await MysqlService.addCarousel(data.name, data.parentId)

async def onDeleteCarousel(request):
     isValid, data = DeleteCarouselValidate(request)
     if not isValid:
          return jsonify({'status': -1, 'msg': f'Invalid input - {data}'})
     return await MysqlService.deleteCarousel(data.id)

async def onUpdateCarouselId(request):
     isValid, data = UpdateItemParentIdValidate(request)
     if not isValid:
          return jsonify({'status': -1, 'msg': f'Invalid input - {data}'})
     return await MysqlService.updateCarouselParentId(data.originalParentId, data.newParentId)