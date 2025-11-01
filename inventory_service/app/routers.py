import os
from fastapi import APIRouter, Depends, HTTPException, Header
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

@router.post("/inventory", response_model=schemas.InventoryOut)
def add_inventory(item: schemas.InventoryCreate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    inv = db.query(models.Inventory).filter(
        models.Inventory.product_id == item.product_id,
        models.Inventory.warehouse == (item.warehouse or "default")
    ).first()
    if inv:
        inv.quantity += item.quantity
    else:
        inv = models.Inventory(product_id=item.product_id, quantity=item.quantity, warehouse=item.warehouse)
        db.add(inv)
    db.commit()
    db.refresh(inv)
    return inv

@router.get("/inventory/{product_id}", response_model=list[schemas.InventoryOut])
def get_inventory(product_id: int, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    invs = db.query(models.Inventory).filter(models.Inventory.product_id == product_id).all()
    if not invs:
        raise HTTPException(status_code=404, detail="not found")
    return invs

@router.post("/inventory/adjust/{product_id}", response_model=schemas.InventoryOut)
def adjust_inventory(product_id: int, adjust: int, warehouse: str | None = None, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    wh = warehouse or "default"
    inv = db.query(models.Inventory).filter(models.Inventory.product_id == product_id, models.Inventory.warehouse == wh).first()
    if not inv:
        raise HTTPException(status_code=404, detail="not found")
    inv.quantity += adjust
    db.commit()
    db.refresh(inv)
    return inv
