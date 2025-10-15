from models.schemas import Product, ProductList
from abc import ABC, abstractmethod

class ProductServiceInterface(ABC):
    @abstractmethod
    async def get_products(self) -> ProductList:
        raise NotImplementedError