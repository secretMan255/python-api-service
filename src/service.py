from ApiBase.ApiBase import ApiBase
from MysqlBase.MysqlBase import MysqlService
from googleCloudStorage.storage import GoogleCloudStorage

class Service:
     def __init__(self, host: str = None, port: int = None):
          self.host = host
          self.port = port
          ApiBase()

     @classmethod
     async def async_init(cls, host: str = None, port: int = None):
          instance = cls(host, port)
          instance.load_endpoints()
          await instance.ServiceStart()
          return instance

     async def ServiceStart(self):
          await GoogleCloudStorage.init()
          await MysqlService.init()
          await ApiBase.start(self.host, self.port)

     @classmethod
     def load_endpoints(cls):
          try:
               import AdminEndpoint.v1.endpoint
          except Exception as err:
               print(f"Failed to load endpoints: {err}")