import os
import sys
import uvicorn

from fastapi import FastAPI
from .routers import router as inventory_router


sys.path.append(os.path.dirname(__file__))

app = FastAPI(title="Inventory Service")
app.include_router(inventory_router, prefix="/api")

@app.get("/")
def root():
    return {"service": "inventory"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)
