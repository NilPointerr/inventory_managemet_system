import uvicorn

from fastapi import FastAPI
from .routers import router as product_router


app = FastAPI(title="Product Service")
app.include_router(product_router, prefix="/api")

@app.get("/")
def root():
    return {"service": "product"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8002, reload=True)
