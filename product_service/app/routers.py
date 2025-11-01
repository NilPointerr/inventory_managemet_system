import os
from fastapi import APIRouter, Depends, HTTPException, Header, Query
from sqlalchemy.orm import Session
from jose import jwt
from dotenv import load_dotenv

from .database import SessionLocal, engine, Base
from . import models, schemas

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env'))
SECRET = os.getenv('JWT_SECRET', 'secret')
ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')

router = APIRouter()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(authorization: str | None = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="missing token")
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="invalid auth scheme")
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="invalid token")

@router.post("/products", response_model=schemas.ProductOut)
def create_product(p: schemas.ProductCreate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    prod = models.Product(name=p.name, description=p.description, price=p.price, category=p.category)
    db.add(prod)
    db.commit()
    db.refresh(prod)
    return prod

@router.get("/products", response_model=list[schemas.ProductOut])
def list_products(
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    category: str | None = Query(None)
):
    q = db.query(models.Product)
    if category:
        q = q.filter(models.Product.category == category)
    offset = (page - 1) * per_page
    return q.offset(offset).limit(per_page).all()

@router.get("/products/{product_id}", response_model=schemas.ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    prod = db.get(models.Product, product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="not found")
    return prod

@router.put("/products/{product_id}", response_model=schemas.ProductOut)
def update_product(product_id: int, p: schemas.ProductCreate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    prod = db.get(models.Product, product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="not found")
    prod.name = p.name
    prod.description = p.description
    prod.price = p.price
    prod.category = p.category
    db.commit()
    db.refresh(prod)
    return prod

@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    prod = db.get(models.Product, product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="not found")
    db.delete(prod)
    db.commit()
    return {"ok": True}
