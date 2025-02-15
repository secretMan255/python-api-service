from pydantic import BaseModel, Field, ValidationError
from typing import Optional, List

class LoginResuest(BaseModel):
     username: str
     password: str
     role: str

class UpdateProductDescribe(BaseModel):
     productId: int
     describe: str

class UpdateProductDetail(BaseModel):
     productId: int
     productName: Optional[str] = None
     parentId: Optional[str] = None
     icon: Optional[str] = None

class UpdateProductStatus(BaseModel):
     productId: List[int]
     status: int

class DeleteProduct(BaseModel):
     productId: List[int]

class AddProduct(BaseModel):
     productName: str
     parentId: Optional[int] = None
     icon: Optional[str] = None
     describe: Optional[str] = None

class UpdateProductParentId(BaseModel):
     originalParentId: int
     newParentId: int

class UpdateItemDetail(BaseModel):
     itemId: int
     itemName: str
     itemParentId: int
     itemPrice: float
     itemQty: int
     itemImg: str

def LoginValidate(data):
     try:
          return True, LoginResuest(**data)
     except ValidationError as err:
          return False, err.json()
     
def UpdateProductDescribeValidate(data):
     try:
          return True, UpdateProductDescribe(**data)
     except ValidationError as err:
          return False, err.json()
     
def UpdateProductDetailValidate(data):
     try:
          return True, UpdateProductDetail(**data)
     except ValidationError as err:
          return False, err.json()
     
def UpdateProductStatusValidate(data):
     try:
          return True, UpdateProductStatus(**data)
     except ValidationError as err:
          return False, err.json()
     
def DeleteProductValidate(data):
     try:
          return True, DeleteProduct(**data)
     except ValidationError as err:
          return False, err.json()
     
def UpdateProductParentIdValidate(data):
     try:
          return True, UpdateProductParentId(**data)
     except ValidationError as err:
          return False, err.json()

def AddProductValidate(data):
     try:
          return True, AddProduct(**data)
     except ValidationError as err:
          return False, err.json()
     
def UpdateItemDetailValidate(data):
     try:
          return True, UpdateItemDetail(**data)
     except ValidationError as err:
          return False, err.json()