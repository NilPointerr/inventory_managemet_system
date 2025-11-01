import os
import sys
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv


from .database import SessionLocal, engine, Base
from . import models, schemas, crud

# --- Fix Python path so imports work when running locally ---
sys.path.append(os.path.dirname(__file__))

load_dotenv('../../.env')
SECRET = os.getenv('JWT_SECRET')
ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
ACCESS_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '60'))


router = APIRouter()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/register', response_model=schemas.UserOut)
def register(u: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_username(db, u.username)
    if existing:
        raise HTTPException(status_code=400, detail='username taken')
    user = crud.create_user(db, u.username, u.password)
    return user


@router.post('/login', response_model=schemas.Token)
def login(u: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, u.username)
    if not user or not crud.verify_password(u.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='invalid credentials')
    expire = datetime.now() + timedelta(minutes=ACCESS_MINUTES)
    payload = {"sub": user.username, "exp": expire}
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}