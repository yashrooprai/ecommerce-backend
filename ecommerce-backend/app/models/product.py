# models/product.py
from pydantic import BaseModel, Field
from typing import Optional

class Product(BaseModel):
    id: Optional[str] = None
    name: str = Field(default="Laptop")
    description: str = Field(default="High-end gaming laptop")
    price: float = Field(default=1200.50)
    stock: int = Field(default=10)

class ProductInDB(Product):
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class ProductFilter(BaseModel):
    name: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    min_stock: Optional[int] = None
    max_stock: Optional[int] = None