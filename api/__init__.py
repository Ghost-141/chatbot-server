from fastapi import APIRouter
from api import chat, products


api_router = APIRouter()

# include routers
api_router.include_router(auth.router)
api_router.include_router(mongodb_health.router)
api_router.include_router(chat.router)
api_router.include_router(sessions.router)
api_router.include_router(rca.router)
