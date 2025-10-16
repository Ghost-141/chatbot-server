import json
import logging

from core.config import PRODUCTS_JSON_PATH
from models.schemas import ProductList
from services.interface.product_interface import ProductServiceInterface

logger = logging.getLogger(__name__)

class ProductService(ProductServiceInterface):
    async def get_products(self) -> ProductList:
        logger.info("Fetching product data from JSON file.")
        data = self._read_products_file()
        try:
            validated_data = ProductList.model_validate(data)
            logger.info("Product data successfully validated.")
            return validated_data
        except Exception as e:
            logger.error(f"Failed to validate product data: {e}")
            raise ValueError(f"Unable to validate the product schema")

    def _read_products_file(self) -> dict:
        logger.info(f"Reading products from {PRODUCTS_JSON_PATH}")
        with PRODUCTS_JSON_PATH.open("r", encoding="utf-8") as file:
            logger.info("File Loaded Sucessfully.")
            return json.load(file)
