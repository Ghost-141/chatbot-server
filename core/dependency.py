from functools import lru_cache

from services.interface.chat_interface import ChatServiceInterface
from services.interface.product_interface import ProductServiceInterface
from services.chatbot_service import ChatService
from services.product_service import ProductService


@lru_cache()
def get_chat_service() -> ChatServiceInterface:
    return ChatService()

@lru_cache()
def get_product_service() -> ProductServiceInterface:
    return ProductService()
