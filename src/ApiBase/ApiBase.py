import datetime
import os
import jwt
import traceback
from functools import wraps
from dotenv import load_dotenv
from flask import Flask, request, jsonify, g, send_file
from flask_cors import CORS
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
               self.app = Flask(__name__ or "default_app")
               self.app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
               self.app.url_map.strict_slashes = False

               self.app.register_error_handler(Exception, self.error_handler)

               load_dotenv()

               # cors config
               CORS(self.app, origins=os.getenv('ALLOWED_ORIGINS', '*'))
          
          # token secret
          self.secret_key = os.getenv('SECRET_KEY')
          if not self.secret_key:
               raise Exception('SECRET_KEY enviroment variable required')
          
          print('API initialize ...')

     # start api service
     @classmethod
     def start(cls, host: str = None, port: int = None):
          cls.checkInit()

          resolveHost = os.getenv('HOST', host or '127.0.0.1')
          resolvePort = int(os.getenv('PORT', port or 8080))
          print('API service started ...')
          cls.app.run(
               host= resolveHost,
               port= resolvePort
          )

     # generate token
     @classmethod
     def generate_token(cls, payload: dict, expiresIn: int = None) -> str:
          cls.checkInit()
          
          if expiresIn is None:
               expiresIn = os.getenv('EXPIRES_IN', '3600')

          payloadCopy = payload.copy()
          payloadCopy['exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=expiresIn)

          return jwt.encode(payload, cls.secret_key, algorithm='HS256')

     # get endpoint
     @classmethod
     def get(cls, endpoint: str, handler, allowedRoles: list, authType: Auth):
          cls.checkInit()

          @wraps(handler)
          def wrapped(*args, **kwargs):
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
                    result = handler(request)
                    print(f'Result: {result}')

                    if isinstance(result, dict) and result.get('type') == ResultType.IMAGE.value:
                         return send_file(result.get('image'), mimetype='image/jpeg')
                    else:
                         return jsonify({'ret': Res.SUCCESS.value, 'data': result}), 200
               except Exception as err:
                    print(f'API GET error: {err}')
                    return jsonify({'ret': Res.FAIL.value, 'msg': str(err)}), 500
          cls.app.route(endpoint, methods=['GET'])(wrapped)
     
     # post endpoint
     @classmethod
     def post(cls, endpoint: str, handler, allowedRoles: list, authType: Auth):
          cls.checkInit()
          
          @wraps(handler)
          def wrapped(*args, **kwargs):
               authMiddleware = cls.autheticationMiddleware(authType)
               authResponse = authMiddleware()

               if authResponse is not None:
                    return authResponse
               
               roleResponse = cls.roleAuthentication(allowedRoles)
               if roleResponse is not None:
                    return roleResponse

               try:
                    print("Request Headers:", request.headers)
                    print("Query Parameters:", request.args)
                    print("Request JSON:", request.get_json())
                    result = handler(request)
                    print("Result:", result)

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
                         print('not found')
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

               for field in ['role', 'id', 'email', 'name']:
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