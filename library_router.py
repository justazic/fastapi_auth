from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import crud, schemas, auth, models
from fastapi_jwt_auth2 import AuthJWT

lib_router = APIRouter()

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()
    
    
@lib_router.post('/books', status_code=status.HTTP_201_CREATED)
def add_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book)

@lib_router.post('/books')
def list_books(db: Session = Depends(get_db)):
    return crud.get_all_books(db)

@lib_router.post("/comments")
def post_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_username = Authorize.get_jwt_subject()
    db_user = db.query(models.User).filter(models.User.username == current_username).first()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")

    return crud.add_comment(db, comment, user_id=db_user.id)