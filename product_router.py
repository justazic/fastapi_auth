from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import ProductCreate, ProductResponse
import crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@router.post("/")
def create(product: ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)


@router.get("/")
def get_all(product_id: int, db: Session = Depends(get_db)):
    return crud.get_product(db, product_id)


@router.get("/{product_id}")
def get_one(product_id: int, db: Session = Depends(get_db)):
    return crud.get_product(db, product_id)

@router.put("/{product_id}", response_model=ProductResponse)
def update(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    updated = crud.update_product(db, product_id, product)
    # if not updated:
    #     raise HTTPException(status_code=404, detail="Product topilmadi")
    # return updated


@router.delete("/{product_id}")
def delete(product_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product topilmadi")
    return deleted