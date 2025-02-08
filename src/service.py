from ApiBase.ApiBase import ApiBase
from commond.commond import Auth

class Service:
     @classmethod
     def __init__(self, host: str = None, port: int = None):
          self.host = host
          self.port = port
          ApiBase()
          self.adminEndpoint()
          self.ServiceStart()

     @classmethod
     def ServiceStart(cls):
          ApiBase.start(cls.host, cls.port)

     @classmethod
     def adminEndpoint(cls):
          ApiBase.get('/test', cls.test, ['admin'], Auth.Bearer)

     @staticmethod
     def test(request):
          return 'test test'
