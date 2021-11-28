from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from pydantic.networks import EmailStr 

class PostBase(BaseModel):
  title: str
  content: str
  published: bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
  id:int
  email:EmailStr
  created_at:datetime
  class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    created_at:datetime
    user_id: int
    owner:UserOut
    class Config:
        orm_mode = True

class PostOut(BaseModel):
  Post:Post
  Votes:int
  class Config:
        orm_mode = True

class UserCreate(BaseModel):
  email:EmailStr
  password:str
  

     
class LoginUser(BaseModel):
  email:EmailStr
  password: str

class Token(BaseModel):          #Token send by the client.
  access_token:str
  token_type:str

class TokenData(BaseModel):   #The data we embed in to our accesstoken.
  id:Optional[str] = None

class Vote(BaseModel):
  post_id:int
  dir:bool
