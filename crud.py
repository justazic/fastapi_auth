from urllib import response

from sqlalchemy.orm import Session
from models import Product
from schemas import ProductCreate
from fastapi import HTTPException, status

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