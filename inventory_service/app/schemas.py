from pydantic import BaseModel

class InventoryCreate(BaseModel):
    product_id: int
    quantity: int
    warehouse: str | None = "default"

class InventoryOut(InventoryCreate):
    id: int
    class Config:
        orm_mode = True
