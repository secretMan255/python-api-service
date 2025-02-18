from pydantic import BaseModel, Field, ValidationError
from typing import Dict, Optional, List

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

class UpdateItemDescribe(BaseModel):
     itemId: int
     itemDescribe: str

class UpdateItemStatus(BaseModel):
     itemId: List[int]
     status: int

class DeleteItem(BaseModel):
     itemId: List[int]

class UpdateItemParentId(BaseModel):
     originalParentId: int
     newParentId: int

class AddItem(BaseModel):
     itemName: str
     parentId: int
     quantity: int
     price: int
     image: str
     describe: str

class UpdateCarousel(BaseModel):
     id: int
     name: str
     parentId: int

class AddCarousel(BaseModel):
     name: str
     parentId: int

class DeleteCarousel(BaseModel):
     id: List[int]

class DeleteMainProduct(BaseModel):
     id: List[int]

class AddMainProduct(BaseModel):
     id: int

class UploadCloudFile(BaseModel):
     fileName: str
     fileData: str

class DeleteCloudFile(BaseModel):
     fileName: List[str]

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
     
def UpdateItemDescribeValidate(data):
     try:
          return True, UpdateItemDescribe(**data)
     except ValidationError as err:
          return False, err.json()
     
def UpdateItemStatusValidate(data):
     try:
          return True, UpdateItemStatus(**data)
     except ValidationError as err:
          return False, err.json()
     
def DeleteItemValidate(data):
     try:
          return True, DeleteItem(**data)
     except ValidationError as err:
          return False, err.json()
     
def UpdateItemParentIdValidate(data):
     try:
          return True, UpdateItemParentId(**data)
     except ValidationError as err:
          return False, err.json()

def AddItemValidate(data):
     try:
          return True, AddItem(**data)
     except ValidationError as err:
          return False, err.json()

def UpdateCarouselParentIdValidate(data):
     try:
          return True, UpdateItemParentId(**data)
     except ValidationError as err:
          return False, err.json()

def CarouselValidate(data):
     try:
          return True, UpdateCarousel(**data)
     except ValidationError as err:
          return False, err.json()
     
def AddCarouselValidate(data):
     try:
          return True, AddCarousel(**data)
     except ValidationError as err:
          return False, err.json()
     
def DeleteCarouselValidate(data):
     try:
          return True, DeleteCarousel(**data)
     except ValidationError as err:
          return False, err.json()
     
def DeleteMainProductValidate(data):
     try:
          return True, DeleteMainProduct(**data)
     except ValidationError as err:
          return False, err.json()
     
def AddMainProductValidate(data):
     try:
          return True, AddMainProduct(**data)
     except ValidationError as err:
          return False, err.json()
     
def UploadCloudFileValidate(data):
     try:
          return True, UploadCloudFile(**data)
     except ValidationError as err:
          return False, err.json()
     
def DeleteCloudFileValidate(data):
     try:
          return True, DeleteCloudFile(**data)
     except ValidationError as err:
          return False, err.json()