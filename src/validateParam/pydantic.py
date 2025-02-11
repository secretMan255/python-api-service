from pydantic import BaseModel, Field, ValidationError

class LoginResuest(BaseModel):
     username: str
     password: str
     role: str


def LoginValidate(data):
     try:
          return True, LoginResuest(**data)
     except ValidationError as err:
          return False, err.json()