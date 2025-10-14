from fastapi import APIRouter, Depends

router = APIRouter(prefix="/products", tags=["products"])

@router.post('get_products')
async def start_chat() -> None: