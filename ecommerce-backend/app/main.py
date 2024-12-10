from fastapi import FastAPI
from app.routers import auth
from app.routers import product

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(product.router, prefix="/api", tags=["products"])