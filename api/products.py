from fastapi import APIRouter, Depends

from core.dependency import get_product_service
from models.schemas import ProductList
from services.interface.product_interface import ProductServiceInterface

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=ProductList)
async def get_products(
    product_service: ProductServiceInterface = Depends(get_product_service),
) -> ProductList:
    return await product_service.get_products()
