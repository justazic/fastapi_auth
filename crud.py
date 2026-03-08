from urllib import response

from sqlalchemy.orm import Session
from models import Product, Category, Genre, Book, Comment
from schemas import ProductCreate
from fastapi import HTTPException, status
import models, schemas

def create_product(db: Session, product: ProductCreate):
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    response = {
        "status": "201",
        "message": "product yaratildi",
        "name": product.name,
    }
    return response

def get_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product topilmadi")
    response = {
        "status": "200",
        "message": "product topildi",
        "data": product
    }
    return response


def update_product(db: Session, product_id: int, product: ProductCreate):
    db_product = get_product(db, product_id)
    if not db_product:
        return None
    
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)
    if not db_product:
        return None
    
    db.delete(db_product)
    db.commit()
    return db_product


def create_category(db: Session, name: str):
    category = Category
    db.add(category)
    db.commit()
    db.refresh(Category)
    return category

def create_book(db: Session, book_data: schemas.BookCreate):
    new_book = Book(**book_data.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

def get_all_books(db: Session):
    return db.query(Book).all

def add_comment(db: Session, comment_data: schemas.CommentCreate, user_id: int):
    new_comment = models.Comment(
        text=comment_data.text,
        book_id=comment_data.book_id,
        user_id=user_id  
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment