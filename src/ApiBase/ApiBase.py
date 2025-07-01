import datetime
import os
from typing import Callable
import jwt
import traceback
from functools import wraps
from dotenv import load_dotenv
from quart import Quart, request, jsonify, Response, g, send_file
from quart_cors import cors
from enum import Enum
# from ..commond.commond import Auth, ResultType
from commond.commond import Auth, ResultType

class Res(Enum):
     SUCCESS = 0
     FAIL = -1

class ApiBase:
     app = None
     secret_key = None

     # init api service
     @classmethod
     def __init__(self):
          if self.app is None: 
               self.app = Quart(__name__ or "default_app")
               self.app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
               self.app.url_map.strict_slashes = False

               self.app.register_error_handler(Exception, self.error_handler)

               load_dotenv()
               # cors config
               self.app = cors(self.app, allow_origin=["http://localhost:3000","http://127.0.0.1:3000"], allow_credentials=True, allow_headers=["Content-Type", "Authorization"],expose_headers=["Set-Cookie"],allow_methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"])

          
          # token secret
          self.secret_key = os.getenv('SECRET_KEY')
          if not self.secret_key:
               raise Exception('SECRET_KEY enviroment variable required')
          
          print('API initialize ...')

     # Start API Service
     @classmethod
     async def start(cls, host: str = None, port: int = None):
          cls.checkInit()
          resolveHost = os.getenv('HOST', '0.0.0.0')
          resolvePort = os.getenv('PORT') # int(os.getenv('PORT', port or 8080))
          print('API service started...')
          
          await cls.app.run_task(host=resolveHost, port=resolvePort)

     # generate token
     @classmethod
     def generateToken(cls, payload: dict, expiresIn: int = None) -> str:
          cls.checkInit()
          
          if expiresIn is None:
               expiresIn = int(os.getenv('EXPIRES_IN', '3600'))

          payloadCopy = payload.copy()
          payloadCopy['exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=expiresIn)

          return jwt.encode(payload, cls.secret_key, algorithm='HS256')

     # get endpoint
     @classmethod
     def get(cls, endpoint: str, handler: Callable, allowedRoles: list, authType: Auth):
          cls.checkInit()

          @wraps(handler)
          async def wrapped(*args, **kwargs):
               authResponse = cls.autheticationMiddleware(authType)

               if authResponse is not None:
                    return authResponse
               
               roleResponse = cls.roleAuthentication(allowedRoles)
               if roleResponse is not None:
                    return roleResponse
               
               try: 
                    print(f'Request Headers: {request.headers}')
                    print(f'Query Parameters: {request.args}')
                    print(f'Route Parameters: {kwargs  }')
                    result = await handler(request)
                    print(f'Result: {result}')

                    if isinstance(result, dict) and result.get('type') == ResultType.IMAGE.value:
                         return await send_file(result.get('image'), mimetype='image/jpeg')
                    else:
                         if result is not None:
                              if isinstance(result, list):
                                   jsonResult = result
                              elif isinstance(result, dict):
                                   jsonResult = result
                              else:
                                   raise TypeError(f"Unexpected result type: {type(result)}")  # Debugging check

                              # Check if response contains an error
                              if isinstance(jsonResult, dict) and 'res' in jsonResult and 'errMsg' in jsonResult:
                                   return jsonify({'ret': Res.FAIL.value, 'data': jsonResult}), 500

                              return jsonify({'ret': Res.SUCCESS.value, 'data': jsonResult}), 200
               except Exception as err:
                    print(f'API GET error: {err}')
                    return jsonify({'ret': Res.FAIL.value, 'msg': str(err)}), 500
          cls.app.route(endpoint, methods=['GET'])(wrapped)
     
     # post endpoint
     @classmethod
     def post(cls, endpoint: str, handler: Callable, allowedRoles: list, authType: Auth):
          cls.checkInit()
          @wraps(handler)
          async def wrapped(*args, **kwargs):
               authResponse = cls.autheticationMiddleware(authType)

               if authResponse is not None:
                    return authResponse
               
               roleResponse = cls.roleAuthentication(allowedRoles)
               if roleResponse is not None:
                    return roleResponse

               try:
                    print("Request Headers:", request.headers)
                    print("Query Parameters:", request.args)
                    json_data = await request.get_json()
                    print("Request JSON:", json_data)

                    result = await handler(json_data)
                    print("Result:", result)

                    if isinstance(result, dict):
                         return jsonify({'ret': Res.SUCCESS.value, 'data': result}), 200
                    
                    if isinstance(result, Response):  
                         return result

                    if hasattr(result, "json") and callable(getattr(result, "json", None)):
                         jsonResult = await result.json()

                         if 'res' in jsonResult and 'errMsg' in jsonResult:
                              return jsonify({'ret': Res.FAIL.value, 'data': jsonResult}), 500

                         return jsonify({'ret': Res.SUCCESS.value, 'data': jsonResult}), 200

                    return jsonify({'ret': Res.SUCCESS.value, 'data': result}), 200
               except Exception as e:
                    print("API POST error:", e)
                    return jsonify({'ret': Res.FAIL.value, 'msg': str(e)}), 500
          cls.app.route(endpoint, methods=['POST'])(wrapped)
     
     # authentication middleware
     @classmethod
     def autheticationMiddleware(cls, authType: Auth):
          if authType == Auth.Bearer:
               return cls.tokenAuthentication()
          elif authType == Auth.Cookie:
               return cls.cookieAuthentication()
          elif authType == Auth.NoneAuth:
               return lambda: None
          else: raise Exception(f'Unsupported authentication type: { authType }')

     @classmethod
     def tokenAuthentication(cls):
          authHeader = request.headers.get('Authorization')
          if authHeader and authHeader.startswith('Bearer '):
               token = authHeader.split(' ')[1].strip()
               try:
                    payload = jwt.decode(token, cls.secret_key, algorithms=['HS256'])
                    if 'role' not in payload:
                         return jsonify({'ret': Res.FAIL.value, 'msg': 'role is required'}), 401

                    g.authUser = payload
               except jwt.ExpiredSignatureError:  
                    return jsonify({'ret': Res.FAIL.value, 'msg': 'Token expired'}), 401
               except jwt.InvalidTokenError:
                    return jsonify({'ret': Res.FAIL.value, 'msg': 'Invalid token'}), 401
          else:
               return jsonify({'ret': Res.FAIL.value, 'msg': 'Bearer token required'}), 401
          
          return None
     
     @classmethod
     def cookieAuthentication(cls):
          token = request.cookies.get('authToken')
          if not token:
               return jsonify({'ret': Res.FAIL.value, 'msg': 'Cookie token required'}), 401
          try:
               payload = jwt.decode(token, cls.secret_key, algorithms=['HS256'])

               for field in ['role', 'id', 'username']:
                    if field not in payload:
                         return jsonify({'ret': Res.FAIL.value, 'msg': f'{field} is required'}), 401
                    
               g.authUser = payload
          except jwt.ExpiredSignatureError:
               return jsonify({'ret': Res.FAIL.value, 'msg': 'Token expired'}), 401
          except jwt.InvalidTokenError:
               return jsonify({'ret': Res.FAIL.value, 'msg':'Invalid token'}), 401
          
          return None

     @staticmethod
     def roleAuthentication(allowedRoles: list):
          authUser = getattr(g, 'authUser', None)

          if not authUser or not authUser.get('role'):
               return jsonify({'ret': Res.FAIL.value, 'msg': 'Access Denied: No role assigned'}), 403
          if authUser['role'] not in allowedRoles:
               return jsonify({'ret': Res.FAIL.value, 'msg': 'Access Denied: Insufficient permissions'}), 403
          
          return None

     # check api servoce init
     @classmethod
     def checkInit(cls):
          if cls.app is None:
               raise Exception('API service is not init...')

     @staticmethod
     def error_handler(err):
          print("Internal Server Error:", traceback.format_exc())
          return jsonify({'ret': Res.FAIL.value, 'msg': 'Internal server error'}), 500