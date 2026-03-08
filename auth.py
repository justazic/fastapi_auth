from fastapi import HTTPException, status
from models import User
from schemas import SignUpSchema, LoginSchema, ProfileUpdateSchema, ResetPasswordSchema
from fastapi_jwt_auth2 import AuthJWT
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi.encoders import jsonable_encoder
from werkzeug.security import generate_password_hash, check_password_hash
from shared import REFRESH_TOKEN_EXPIRATION_TIME, ACCESS_TOKEN_EXPIRATION_TIME


async def sign_up(data: SignUpSchema, db: Session):
    # db_username = db.query(User).filter(User.username == data.username).first()
    # if db_username:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bunday username mavjud")
    # db_email = db.query(User).filter(User.email == data.email).first()
    # if db_email:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bunday email mavjud")
    
    db_user = db.query(User).filter(or_(User.username == data.username, User.email == data.email)).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bunday username yoki email mavjud")
    
    new_user = User(
        username=data.username,
        email=data.email,
        password=generate_password_hash(data.password),
        name=data.name,
        age=data.age
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "status": "201",
        "message": "User yaratildi",
        "data": {
            "username": new_user.username,
            "email": new_user.email,
            "name": new_user.name
        }
    }
    
def login_user(db: Session, user: LoginSchema, Authorize: AuthJWT):
    db_user = db.query(User).filter(or_(User.username == user.username_or_email,User.email == user.username_or_email)).first()

    if not db_user or not check_password_hash(db_user.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username yoki parol noto'g'ri")

    access_token = Authorize.create_access_token(subject=db_user.username, expires_time=ACCESS_TOKEN_EXPIRATION_TIME)
    refresh_token = Authorize.create_refresh_token(subject=db_user.username, expires_time=REFRESH_TOKEN_EXPIRATION_TIME)

    return jsonable_encoder({
        "status": status.HTTP_200_OK,
        "message": "Login muvaffaqiyatli",
        "access_token": access_token,
        "refresh_token": refresh_token
    })


def refresh_access_token(db: Session, Authorize: AuthJWT):
    try:
        Authorize.jwt_refresh_token_required()
        current_user = Authorize.get_jwt_subject()

        db_user = db.query(User).filter(User.username == current_user).first()
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Foydalanuvchi topilmadi")

        new_access_token = Authorize.create_access_token(subject=current_user, live_time=ACCESS_TOKEN_EXPIRATION_TIME)

        return jsonable_encoder({
            "status": status.HTTP_200_OK,
            "msg": "Access token yangilandi",
            "access_token": new_access_token
        })
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Yaroqsiz refresh token")


def profile(db: Session, Authorize: AuthJWT):
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()

        db_user = db.query(User).filter(User.username == current_user).first()
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Foydalanuvchi topilmadi")

        return jsonable_encoder({
            "status": status.HTTP_200_OK,
            "data": {
                "name": db_user.name,
                "username": db_user.username,
                "email": db_user.email
            }
        })
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Yaroqsiz token")

    

def update_profile(db: Session, Authorize: AuthJWT, profile_data: ProfileUpdateSchema):
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()

        db_user = db.query(User).filter(User.username == current_user).first()
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Foydalanuvchi topilmadi")

        if profile_data.username:
            db_user.username = profile_data.username
        if profile_data.email:
            db_user.email = profile_data.email
        if profile_data.name:
            db_user.name = profile_data.name

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return jsonable_encoder({
            "status": status.HTTP_200_OK,
            "message": "Profil muvaffaqiyatli yangilandi",
            "data": {
                "name": db_user.name,
                "username": db_user.username,
                "email": db_user.email
            }
        })
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Yaroqsiz token")



def reset_password(db: Session, Authorize: AuthJWT, password_data: ResetPasswordSchema):
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()

        db_user = db.query(User).filter(User.username == current_user).first()
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Foydalanuvchi topilmadi")

        if not check_password_hash(db_user.password, password_data.old_password):raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Eski parol noto'g'ri")

        if password_data.new_password != password_data.confirm_password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Yangi parollar mos kelmadi")

        db_user.password = generate_password_hash(password_data.new_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return jsonable_encoder({
            "status": status.HTTP_200_OK,
            "message": "Parol muvaffaqiyatli yangilandi"
        })
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Yaroqsiz token")