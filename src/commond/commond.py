import bcrypt
from enum import Enum

class Auth(Enum):
     Bearer = 'Bearer'
     Cookie = 'Cookie'
     NoneAuth = 'None'

class ResultType(Enum):
    NORMAL = 'NORMAL'
    IMAGE = 'IMAGE'

def compareHash(inputPass, dbPass):
     return bcrypt.checkpw(inputPass.encode('utf-8'), dbPass.encode('utf-8'))