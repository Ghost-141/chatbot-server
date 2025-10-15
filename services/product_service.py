import json

from core.config import PRODUCTS_JSON_PATH
from models.schemas import ProductList
from services.interface.product_interface import ProductServiceInterface


class ProductService(ProductServiceInterface):
    async def get_products(self) -> ProductList:
        data = self._read_products_file()
        return ProductList.model_validate(data)

    @staticmethod
    def _read_products_file() -> dict:
        with PRODUCTS_JSON_PATH.open("r", encoding="utf-8") as file:
            return json.load(file)
