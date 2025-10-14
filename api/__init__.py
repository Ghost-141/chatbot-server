from fastapi import APIRouter
from api import chat, products


api_router = APIRouter()

# include routers
api_router.include_router(chat.router)
api_router.include_router(products.router)

