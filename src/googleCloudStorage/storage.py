import os
from typing import List
from google.cloud import storage

class GoogleCloudStorage:
     client = None
     bucket = None

     @classmethod
     async def init(cls):
          if cls.client is None:
               credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
               cls.client = storage.Client()
               cls.bucket = cls.client.bucket(os.getenv('BUCKET'))
               print('Google Cloud Storage Client initialized')

     @classmethod
     async def fileList(cls):
          if cls.client is None:
               cls.init()
          
          blobs = cls.bucket.list_blobs()
          return {'files': [blob.name for blob in blobs]}
     
     @classmethod
     async def deleteFile(cls, fileName: List[str]):
          if cls.client is None:
               cls.init()

          try:
               for name in fileName:
                    blob = cls.bucket.blob(name)
                    blob.delete()
          except Exception as err:
               return {'errMsg' : err}
          
     @classmethod
     async def uploadFile(cls, name: str, fileData: str):
          if cls.client is None:
               cls.init()
          try:
               # data = bytes([fileData[i] for i in sorted(fileData.keys(), key=int)])
               data = bytes.fromhex(fileData)
               blob = cls.bucket.blob(name)
               blob.upload_from_string(data, content_type='image/jpeg')
          except Exception as err:
               return {'errMsg': err}

     