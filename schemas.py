from pydantic import BaseModel, Field
from typing import Optional

class ProductCreate(BaseModel):
    name = Field(min_length=3, max_length=14)
    description: str | None = None
    price = int
    
    
class ProductResponse(BaseModel):
    id: int
    
    class Config:
        from_atributes = True
        
        
class SignUpSchema(BaseModel):
    id: int = Optional
    name: str
    age: int
    email: str = Field(min_length=9, max_length=20)
    username: str = Field(min_length=5, max_length=20)
    password: str = Field(min_length=5, max_length=20)
    
    class Config:
        orm_mode = True
        
        
class Settings(BaseModel):
    authjwt_secret_key: str = "orKT1mkLti6Z7Zy0bl0A"


class LoginSchema(BaseModel):
    username_or_email: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=5, max_length=50)
    
    class Config:
        orm_mode = True

class ProfileUpdateSchema(BaseModel):
    username:str = Optional
    email:str = Optional
    name:str =Optional
    
    class Config:
        orm_mode = True
        
        
class ResetPasswordSchema(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str