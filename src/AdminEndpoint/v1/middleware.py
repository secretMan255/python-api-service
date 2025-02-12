from quart import jsonify, make_response
from ApiBase.ApiBase import ApiBase
from validateParam.pydantic import LoginValidate
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