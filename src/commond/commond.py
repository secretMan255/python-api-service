from enum import Enum

class Auth(Enum):
     Bearer = 'Bearer'
     Cookie = 'Cookie'
     NoneAuth = 'None'

class ResultType(Enum):
    NORMAL = 'NORMAL'
    IMAGE = 'IMAGE'