from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class ChatQuery(BaseModel):
    message: str 

class ChatResponse(BaseModel):
    model_response: str


class Dimensions(BaseModel):
    width: float
    height: float
    depth: float


class Product(BaseModel):
    
    model_config = ConfigDict(extra="allow")

    id: int
    title: str
    description: str
    category: str
    price: float
    discountPercentage: float
    rating: float
    stock: int
    tags: List[str]
    brand: Optional[str] = None
    sku: str
    weight: float
    dimensions: Dimensions


class ProductList(BaseModel):
    model_config = ConfigDict(extra="allow")
    products: List[Product]
    total: Optional[int] = None
    skip: Optional[int] = None
    limit: Optional[int] = None
