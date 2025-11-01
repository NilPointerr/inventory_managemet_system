# from sqlalchemy.orm import Session
# from passlib.context import CryptContext
# from . import models


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def get_user_by_username(db: Session, username: str):
#     return db.query(models.User).filter(models.User.username == username).first()


# def create_user(db: Session, username: str, password: str):
#     hashed = pwd_context.hash(password)
#     user = models.User(username=username, hashed_password=hashed)
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return user


# def verify_password(plain, hashed):
#     return pwd_context.verify(plain, hashed)

from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models
import hashlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _safe_password(password: str) -> str:
    """
    Hash passwords longer than 72 bytes with SHA256 before bcrypt,
    since bcrypt only handles up to 72 bytes safely.
    """
    if len(password.encode("utf-8")) > 72:
        # Pre-hash with SHA256 to shorten safely
        password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return password

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, username: str, password: str):
    password = _safe_password(password)
    hashed = pwd_context.hash(password)
    user = models.User(username=username, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def verify_password(plain: str, hashed: str) -> bool:
    plain = _safe_password(plain)
    return pwd_context.verify(plain, hashed)
