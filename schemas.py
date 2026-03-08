from pydantic import BaseModel, Field
from typing import Optional

class ProductCreate(BaseModel):
    name: str = Field(min_length=3, max_length=14)
    description: str | None = None
    price: int
    
    
class ProductResponse(BaseModel):
    id: int
    
    class Config:
        from_attributes = True
        
        
class SignUpSchema(BaseModel):
    id: int = Optional
    name: str
    age: int
    email: str = Field(min_length=9, max_length=20)
    username: str = Field(min_length=5, max_length=20)
    password: str = Field(min_length=5, max_length=20)
    
    class Config:
        from_attributes = True
        
        
class Settings(BaseModel):
    authjwt_secret_key: str = "orKT1mkLti6Z7Zy0bl0A"


class LoginSchema(BaseModel):
    username_or_email: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=5, max_length=50)
    
    class Config:
        from_attributes = True

class ProfileUpdateSchema(BaseModel):
    username:str = Optional
    email:str = Optional
    name:str =Optional
    
    class Config:
        from_attributes = True
        
        
class ResetPasswordSchema(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str
    
    
class Categoryschema(BaseModel):
    name: str
    
    
class Genreschema(BaseModel):
    name: str
    
    
class BookCreate(BaseModel):
    title: str
    author:str
    description: Optional[str] = None
    category_id: int
    genre_id: int
    
    
class CommentCreate(BaseModel):
    text: str
    book_id: int
    
    
class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    category_id: int
    
    class Config:
        from_attributes = True
        