from ApiBase.ApiBase import ApiBase
from MysqlBase.MysqlBase import MysqlService

class Service:
     @classmethod
     def __init__(self, host: str = None, port: int = None):
          self.host = host
          self.port = port
          MysqlService()
          ApiBase()
          self.load_endpoints()
          self.ServiceStart()

     @classmethod
     def ServiceStart(cls):
          ApiBase.start(cls.host, cls.port)

     @classmethod
     def load_endpoints(cls):
          try:
               import AdminEndpoint.v1.endpoint
          except Exception as err:
               print(f"Failed to load endpoints: {err}")
