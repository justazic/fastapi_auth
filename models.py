from sqlalchemy import Column, Integer, String
from database import Base

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), nullable=False)
    description = Column(String)
    price = Column(Integer, nullable=True)
    
    
class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    age = Column(Integer)
    username = Column(String(20), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(20), nullable=False)
    