import os
import sys

import uvicorn
from fastapi import FastAPI

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from .routers import router as auth_router


app = FastAPI(title="Auth Service")
app.include_router(auth_router, prefix="/auth")

@app.get("/")
def root():
    return {"service": "auth"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

