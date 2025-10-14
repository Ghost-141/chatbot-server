from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class ChatQuery(BaseModel):
    message: str 
    timestamp: datetime

class Dimensions(BaseModel):
    width: float
    height: float
    depth: float


class Product(BaseModel):
    id: int
    title: str
    description: str
    category: str
    price: float
    discountPercentage: float = Field(..., alias="discountPercentage")
    rating: float
    stock: int
    tags: List[str]
    brand: str
    sku: str
    weight: float
    dimensions: Dimensions


class ProductList(BaseModel):
    products: List[Product]