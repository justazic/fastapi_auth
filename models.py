from sqlalchemy import Column, Integer, String, ForeignKey,Text
from database import Base
from sqlalchemy.orm import relationship

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
    
    
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=True)
    books = relationship("Book", back_populates='category')
    

class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=True)
    books = relationship("Book", back_populates='genre')
    
    
class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=True)
    author = Column(String(50))
    description = Column(Text)
    category_id = Column(Integer, ForeignKey('categories.id'))
    genre_id = Column(Integer, ForeignKey('genres.id'))
    category = relationship('Category', back_populates='books')
    genre = relationship('Genre', back_populates='books')
    comments = relationship('Comment', back_populates='books', cascade='all, delete-orphan')
    
    
class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    book = relationship('Book', back_populates='comments')
        